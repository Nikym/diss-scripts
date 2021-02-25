import scipy.io as sio
import numpy as np
import json
import os
from collections import defaultdict

ROOT_PATH = '/Volumes/nik_ext/diss/fat_dataset/fat'

object_ids = defaultdict(lambda: None)
conversion_ids = defaultdict(list)

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
  # i_matrix[0][2] = i_data['cx']
  # i_matrix[1][2] = i_data['cy']
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
  cls_indexes = np.zeros(n, dtype=np.float32)

  for i, obj in enumerate(data['objects']):
    obj_name = obj['class'][:-4]
    cls_indexes[i] = object_ids[obj_name]

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

  for x in range(0, num_of_files):
    for angle in ['left', 'right']:
      index = x
      if angle is 'right':
        index += num_of_files

      file_name = str(x).zfill(6) + '.' + angle + '.json'
      with open(os.path.join(path, file_name)) as f:
        data = json.load(f)

      sio.savemat(output_dir + '/' + str(index + start_index).zfill(6) + '-meta.mat', {
        'center': get_centers(data),
        'factor_depth': get_factor_depth(),
        'intrinsic_matrix': get_intrinsic_matrix(camera_data),
        'poses': get_rt_matrices(data),
        'cls_indexes': get_cls_indexes(data)
      })
  
  # Multiplied by 2 as each scene has two angles
  return num_of_files * 2

def get_directories(root: str = '') -> list:
  '''
  Retrives relative paths to the FAT files.

    Parameters:
      root (str): The root directory of the FAT dataset

    Returns:
      dir_list (list): List of relative paths
  '''

  # Get names of directories at root
  dir_list_mixed = [
    'mixed/' + item for item in os.listdir(ROOT_PATH + '/mixed') if os.path.isdir(os.path.join(ROOT_PATH, 'mixed', item))]
  # Sorted to ensure processed data is always in same order
  dir_list_mixed.sort()

  dir_list_single_objs = [
    'single/' + item for item in os.listdir(ROOT_PATH + '/single') if os.path.isdir(os.path.join(ROOT_PATH, 'single', item))]

  dir_list_single = []
  for directory in dir_list_single_objs:
    dir_list_single.extend(
      [directory + '/' + item for item in os.listdir(ROOT_PATH + '/' + directory) if os.path.isdir(os.path.join(ROOT_PATH, directory, item))]
    )

  dir_list_single.sort()

  dir_list = []
  dir_list.extend(dir_list_mixed)
  dir_list.extend(dir_list_single)

  return dir_list

if __name__ == '__main__':
  print('Creating .mat files...')

  dir_list = get_directories(ROOT_PATH + '/')

  log_file = open('meta_processing_log.txt', 'w+')

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
      'output'
    )
  
  log_file.close()

  with open('object_ids.json', 'w+') as f:
    f.write(json.dumps(object_ids, indent=2))

  with open('conversion_ids.json', 'w+') as f:
    f.write(json.dumps(conversion_ids, indent=2))