import scipy.io as sio
import numpy as np
import json
import os
import cv2
from collections import defaultdict
from shared_resources import ROOT_DIR, OUT_DIR, NUM_SETS, process_mixed, process_single

with open('/home/nikita/diss/scripts/objectIds.json') as f:
    OBJECT_SEG_IDS = json.load(f)

with open(ROOT_DIR + 'mixed/kitchen_0/_camera_settings.json') as f:
    camera_data = json.load(f)

def get_label_ids(data: dict) -> dict:
    '''
    Generates a dictionary of the segmentation IDs in the scene.

        Parameters:
            data (dict): JSON data from scene context
        
        Returns:
            object_ids (dict): Dictionary of name-id pairs
    '''
    object_ids = {}

    for obj in data['exported_objects']:
        obj_name = obj['class']

        object_ids[obj_name] = obj['segmentation_class_id']
    
    return object_ids

def get_objects_in_scene(path: str) -> list:
    '''
    Retrives a list of object names that are in the scene.

        Parameters:
            path (str): Path to box.txt file
        
        Returns:
            obj_list (list): List of object names in scene
    '''
    obj_list = []

    with open(path) as f:
        for line in f.readlines():
            line_list = line.split(' ')
            obj_list.append(line_list[0])
    
    return obj_list

def remove_hidden(data: dict, box_path: str) -> dict:
    '''
    Removes object data if the object instance is out of frame.

        Parameters:
            data (dict): JSON data from the scene
            box_path (str): Path to location of the box.txt file for scene

        Returns:
            data (dict): Updated JSON data from scene
    '''
    obj_list = get_objects_in_scene(box_path)

    new_objs = []
    for obj in data['objects']:
        if obj['class'] in obj_list:
            new_objs.append(obj)
    
    data['objects'] = new_objs
    return data

def get_centers(data: dict) -> np.ndarray:
    '''
    Returns n * 2 numpy array of x,y coords of projected centers of objects in image.
  
        Parameters:
            data (dict): JSON data file from FAT dataset
    
        Returns:
            centers (numpy.ndarray): n * 2 numpy array
    '''
    n = len(data['objects'])
    centers = np.zeros((n, 2), dtype=np.float32)

    for i, obj in enumerate(data['objects']):
        centers[i] = obj['projected_cuboid_centroid']
        # Adjusting for the cropped images
        centers[i][0] -= 160
        centers[i][1] -= 30

    return centers

def get_factor_depth() -> np.ndarray:
    '''
    Return the factor depth parameter.

        Returns:
            factor_depth (numpy.ndarray): 1-D array containing factor depth.
    '''
    return np.array(10000, dtype=np.float64)

def get_intrinsic_matrix(camera_data: dict) -> np.ndarray:
    '''
    Get numpy array of the intrinsic matrix from given JSON.

        Parameters:
            camera_data (dict): Camera JSOn file from NDDS data

        Returns:
            i_matrix (numpy.ndarray): Intrinsic matrix in numpy format
    '''
    i_matrix = np.zeros((3, 3), dtype=np.float64)
    i_data = camera_data['camera_settings'][0]['intrinsic_settings']

    i_matrix[0][0] = i_data['fx']
    i_matrix[1][1] = i_data['fy']
    i_matrix[2][2] = 1
    i_matrix[0][1] = i_data['s']
    i_matrix[0][2] = 320
    i_matrix[1][2] = 240

    return i_matrix

def _get_transpose_permutation(matrix: list) -> np.ndarray:
    '''
    Transposes and permutates the rt matrix stored in the JSON files.

        Parameters:
            matrix (list): List representation of matrix

        Returns:
            rt_matrix (numpy.ndarray): Transposed and permuted matrix
    '''
    rt_matrix = np.array(matrix)

    r_matrix = np.delete(rt_matrix, 3, 0)
    r_matrix = np.delete(r_matrix, 3, 1)

    t_vector = rt_matrix[3][0:3]
    t_vector = t_vector.reshape(-1, 1)
    t_vector = t_vector / 100 # Convert from cm to m

    p = np.zeros((3, 3))
    p[0][2] = 1
    p[1][0] = 1
    p[2][1] = -1

    r_matrix = np.matmul(r_matrix.T, p)
    rt_matrix = np.append(r_matrix, t_vector, axis=1)

    return np.float32(rt_matrix)

def get_rt_matrices(data: dict) -> np.ndarray:
    '''
    Get rotation-translation matrices formated in YCB style.

        Parameters:
            data (dict): JSON object data from meta-data file

        Returns:
            rt_matrices (numpy.ndarray): 3 by 4 by n numpy array
    '''
    rt_matrices = None

    for obj in data['objects']:
        rt_matrix = _get_transpose_permutation(
            obj['pose_transform_permuted']
        )

        if rt_matrices is None:
            rt_matrices = rt_matrix
        else:
            rt_matrices = np.dstack((rt_matrices, rt_matrix))

    if rt_matrices is None:
        return np.array([], dtype=np.float32)

    return rt_matrices

def get_cls_indexes(data: dict) -> np.ndarray:
    '''
    Created array of segmentation IDs in particular image.

        Parameters:
            data (dict): JSON representation of image data

        Returns:
            cls_indexes (numpy.ndarray): Array of segmentation IDs
    '''
    n = len(data['objects'])

    if n is 0:
        return np.array([], dtype=np.float32)
    
    cls_indexes = np.zeros((n,1), dtype=np.float32)

    for i, obj in enumerate(data['objects']):
        obj_name = obj['class']
        cls_indexes[i][0] = OBJECT_SEG_IDS[obj_name]

    return cls_indexes

def change_pixel_value(path: str, frm: int, to: int):
    '''
    Adjusts specified pixel value to new value.

        Parameters:
            path (str): Path to image
            frm (int): Pixel value (0-255)
            to (int): Pixel value (0-255)
    '''
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img[np.where(img == [frm])] = [to]

    cv2.imwrite(path, img)

def update_label_image(path: str, old_ids: dict):
    '''
    Converts old IDs to new IDs in segmentation / label image.
    '''
    for obj_name in old_ids.keys():
        old_id = old_ids[obj_name]
        new_id = OBJECT_SEG_IDS[obj_name[:-4]]

        change_pixel_value(path, old_id, new_id)

def process_scene(scene_path: str, scene_id: str, out_path: str, new_id: str):
    with open(scene_path + '_object_settings.json') as f:
        obj_data = json.load(f)

    with open(scene_path + scene_id + '.json') as f:
        data = remove_hidden(json.load(f), out_path + new_id + '-box.txt')

    old_object_ids = get_label_ids(obj_data)

    # Process label image
    update_label_image(out_path + new_id + '-label.png', old_object_ids)

    # Process mat data
    centers = get_centers(data)
    factor_depth = get_factor_depth()
    intrinsic_matrix = get_intrinsic_matrix(camera_data)
    poses = get_rt_matrices(data)
    cls_indexes = get_cls_indexes(data)

    sio.savemat(out_path + new_id + '-meta.mat', {
        'center': centers,
        'factor_depth': factor_depth,
        'intrinsic_matrix': intrinsic_matrix,
        'poses': poses,
        'cls_indexes': cls_indexes
    })


def main():
    print('*** BEGINNING MAT META FILE CREATION ***')
    try:
        os.mkdir(OUT_DIR[:-1])
    except Exception:
        print('(Directory "processed" already created, skipping creation...)')
    
    id_track = process_mixed(process_scene)
    process_single(id_track, process_scene)

    print('*** COMPLETE ***')

if __name__ == '__main__':
    main()