import scipy.io as sio
import numpy as np
import json
import os

ROOT_PATH = '/Volumes/nik_ext/diss/fat_dataset/fat'

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
  i_matrix = np.empty((3, 3), dtype=np.float64)

  i_data = camera_data['camera_settings'][0]['intrinsic_settings']
  
  i_matrix[0][0] = i_data['fx']
  i_matrix[1][1] = i_data['fy']
  i_matrix[2][2] = 1
  i_matrix[0][1] = i_data['s']
  i_matrix[0][2] = i_data['cx']
  i_matrix[1][2] = i_data['cy']
  i_matrix[1][0] = 0
  i_matrix[2][0] = 0
  i_matrix[2][1] = 0

  # i_matrix[0][0] = '{:e}'.format(i_data['fx'])
  # i_matrix[1][1] = '{:e}'.format(i_data['fy'])
  # i_matrix[2][2] = '{:e}'.format(1)
  # i_matrix[0][1] = '{:e}'.format(i_data['s'])
  # i_matrix[0][2] = '{:e}'.format(i_data['cx'])
  # i_matrix[1][2] = '{:e}'.format(i_data['cy'])
  # i_matrix[1][0] = '{:e}'.format(0)
  # i_matrix[2][0] = '{:e}'.format(0)
  # i_matrix[2][1] = '{:e}'.format(0)

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

if __name__ == '__main__':
  print('Creating .mat files...')

  with open(ROOT_PATH + '/mixed/kitchen_0/000000.right.json') as f:
    data = json.load(f)
  
  with open(ROOT_PATH + '/mixed/kitchen_0/_camera_settings.json') as f:
    camera_data = json.load(f)

  
  get_rt_matrices(data)

  sio.savemat('test.mat', {
    'center': get_centers(data),
    'factor_depth': get_factor_depth(),
    'intrinsic_matrix': get_intrinsic_matrix(camera_data),
    'poses': get_rt_matrices(data)
  })

  print(sio.whosmat('test.mat'))