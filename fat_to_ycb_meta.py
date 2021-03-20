import scipy.io as sio
import numpy as np
import json
import os
from collections import defaultdict
from common_funcs import get_failed_files, get_directories, ROOT_PATH

FAILED_FILES = get_failed_files()

object_ids = defaultdict(lambda: None)
conversion_ids = defaultdict(list)

def get_objects_in_scene(box_path: str) -> list:
  '''
  Retrives list of objects present in a given box annotation file.

    Parameters:
      box_path (str): Path to the relevant box annotation file

    Returns:
      obj_list (list): List of objects present in the box annotation file
  '''
  obj_list = []
  with open(box_path, 'r') as f:
    while True:
      line = f.readline()

      if not line:
        break

      line_list = line.split(' ')
      obj_list.append(line_list[0])

  return obj_list

def pre_process_data(data: dict, path: str) -> dict:
  '''
  Removes objects from dataset that are no longer required.

    Parameters:
      data (dict): JSON representation of the FAT meta file
      path (str): Path to file
    
    Returns:
      data (dict): FAT meta data with missing objects removed
  '''
  obj_list = get_objects_in_scene(path)

  new_obj = []
  for obj in data['objects']:
    if obj['class'][:-4] in obj_list:
      new_obj.append(obj)

  data['objects'] = new_obj
  return data

def generate_label_ids(data: dict):
  '''
  Generates the segmentation / label IDs for each object and stores the
  information in a global dict.

    Parameters:
      data (dict): JSON _object_settings data
  '''
  for obj in data['exported_objects']:
    obj_name = obj['class'][:-4]

    if object_ids[obj_name] is None:
      object_ids[obj_name] = obj['segmentation_class_id']
    elif obj['segmentation_class_id'] not in conversion_ids[object_ids[obj_name]]:
      conversion_ids[object_ids[obj_name]].append(obj['segmentation_class_id'])

def get_centers(data: dict) -> np.ndarray:
  '''
  Returns n * 2 numpy array of x,y coords of projected centers of objects in image.
  
    Parameters:
      data (dict): JSON data file from FAT dataset
    
    Returns:
      centers (numpy.ndarray): n * 2 numpy array
  '''
  n = len(data['objects'])
  centers = np.empty((n, 2), dtype=np.float32)

  for i, obj in enumerate(data['objects']):
    centers[i] = obj['projected_cuboid_centroid']
    centers[i][0] -= 160
    centers[i][1] -= 30

  return centers

def get_factor_depth() -> np.ndarray:
  '''
  Returns the factor depth parameter.

    Returns:
      factor_depth (numpy.ndarray): 0-D array containing factor depth
  '''
  return np.array(10000, dtype=np.float64)

def get_intrinsic_matrix(camera_data: dict) -> np.ndarray:
  '''
  Gets numpy array of the intrinsic matrix from given JSON.

    Parameters:
      camera_data (dict): Camera JSON file from FAT dataset

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
  Transposes and permutates the rt matrix stored in FAT files.

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

  p = np.zeros((3, 3))
  p[1][0] = 1
  p[2][1] = -1
  p[0][2] = 1

  r_matrix = np.matmul(r_matrix.T, p)
  rt_matrix = np.append(r_matrix, t_vector, axis=1)

  return np.float32(rt_matrix)

def get_rt_matrices(data: dict) -> np.ndarray:
  '''
  Get rotation-translation matrices formated in YCB style.

    Parameters:
      data (dict): JSON object data from meta-data file
    
    Returns:
      rt_matrices (numpy.ndarray): 3 * 4 * n numpy array 
  '''
  rt_matrices = None

  for obj in data['objects']:
    fat_rt_matrix = _get_transpose_permutation(
      obj['pose_transform_permuted']
    )

    if rt_matrices is None:
      rt_matrices = fat_rt_matrix
    else:
      rt_matrices = np.dstack((rt_matrices, fat_rt_matrix))

  if rt_matrices is None:
    return np.array([], dtype=np.float32)

  return rt_matrices

def get_cls_indexes(data: dict) -> np.ndarray:
  '''
  Creates array of segmentation IDs features in particular image.

    Parameters:
      data (dict): JSON representation of FAT image data

    Returns:
      cls_indexes (numpy.ndarray): Array of segmentation IDs
  '''
  n = len(data['objects'])

  if n is 0:
    return np.array([], dtype=np.float32)

  cls_indexes = np.zeros((n,1), dtype=np.float32)

  for i, obj in enumerate(data['objects']):
    obj_name = obj['class'][:-4]
    cls_indexes[i][0] = object_ids[obj_name]

  return cls_indexes

def process_scenes(path: str, start_index: int, output_dir: str = 'output') -> int:
  '''
  Processes the meta files in a specified directory and outputs .mat files.

    Parameters:
      path (str): The path of the directory to be processed
      start_index (int): The index at which the output file names should start at
      output_dir (str): The path to the output directory

    Returns:
      num_files_processed (int): The number of files that were processed
  '''
  with open(os.path.join(path, '_camera_settings.json')) as f:
    camera_data = json.load(f)

  with open(os.path.join(path, '_object_settings.json')) as f:
    obj_data = json.load(f)

  generate_label_ids(obj_data)
  
  # Each scene has 2 angles with 4 data files each, plus 2 camera files not related (hence -2)
  num_of_files = int((len(os.listdir(path)) - 2) / 8)

  index = 0
  for x in range(0, num_of_files):
    for angle in ['left', 'right']:
      file_name = str(x).zfill(6) + '.' + angle + '.json'
      # If file does not have processed image then skip
      if os.path.join(path, file_name[0:-5]) in FAILED_FILES:
        continue

      with open(os.path.join(path, file_name)) as f:
        data = json.load(f)

      out_file_id = str(index + start_index).zfill(6)

      data = pre_process_data(
        data,
        os.path.join(ROOT_PATH, 'output', 'box', out_file_id + '-box.txt')
      )

      centers = get_centers(data)
      factor_depth = get_factor_depth()
      intrinsic_matrix = get_intrinsic_matrix(camera_data)
      poses = get_rt_matrices(data)
      cls_indexes = get_cls_indexes(data)

      try:
        sio.savemat(output_dir + '/' + out_file_id + '-meta.mat', {
          'center': centers,
          'factor_depth': factor_depth,
          'intrinsic_matrix': intrinsic_matrix,
          'poses': poses,
          'cls_indexes': cls_indexes
        })
      except Exception:
        print('Error! Print retrived vars:')
        print(centers, '\n')
        print(factor_depth, '\n')
        print(intrinsic_matrix, '\n')
        print(poses, '\n')
        print(cls_indexes, '\n')
      
      index += 1
  
  return index

if __name__ == '__main__':
  print('Creating .mat files...')

  dir_list = get_directories(ROOT_PATH + '/')

  log_file = open(ROOT_PATH + '/output/meta_processing_log.txt', 'w+')

  total_files = 0
  total_dir = len(dir_list)

  log_file.write('Total directories: ' + str(total_dir) + '\n')

  for i, directory in enumerate(dir_list):
    print('Processing ' + directory + ' ... (start @ ' + 
      str(total_files) + ', dir ' + str(i+1) + '/' + str(total_dir) + ')')
    log_file.write('[' + str(total_files).zfill(5) + '] ' + directory + '\n')
    
    path = ROOT_PATH + '/' + directory
    total_files += process_scenes(
      path,
      total_files,
      ROOT_PATH + '/output/mat'
    )
  
  log_file.close()

  with open(ROOT_PATH + '/output/object_ids.json', 'w+') as f:
    f.write(json.dumps(object_ids, indent=2))

  with open(ROOT_PATH + '/output/conversion_ids.json', 'w+') as f:
    f.write(json.dumps(conversion_ids, indent=2))

  print('Complete')