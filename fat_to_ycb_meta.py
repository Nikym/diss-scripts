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
  
  i_matrix[0][0] = '{:e}'.format(i_data['fx'])
  i_matrix[1][1] = '{:e}'.format(i_data['fy'])
  i_matrix[2][2] = '{:e}'.format(1)
  i_matrix[0][1] = '{:e}'.format(i_data['s'])
  i_matrix[0][2] = '{:e}'.format(i_data['cx'])
  i_matrix[1][2] = '{:e}'.format(i_data['cy'])
  i_matrix[1][0] = '{:e}'.format(0)
  i_matrix[2][0] = '{:e}'.format(0)
  i_matrix[2][1] = '{:e}'.format(0)

  # TODO: Sort out the precision of the intrinsic matrix to be higher
  return i_matrix

def get_rt_matrices(data: dict) -> np.ndarray:
  '''
  Get rotation-translation matrices formated in YCB style.

    Parameters:
      data (dict): JSON object data from meta-data file
    
    Returns:
      rt_matrices (numpy.ndarray): 3 * 4 * n numpy array 
  '''
  n = len(data['objects'])
  rt_matrices = np.empty((3, 4, n), dtype=np.float32)

  for obj in data['objects']:
    # TODO: Permutate matrix and put into the weird YCB format
    pass

  return rt_matrices

if __name__ == '__main__':
  print('Creating .mat files...')

  with open(ROOT_PATH + '/mixed/kitchen_0/000000.right.json') as f:
    data = json.load(f)
  
  with open(ROOT_PATH + '/mixed/kitchen_0/_camera_settings.json') as f:
    camera_data = json.load(f)

  sio.savemat('test.mat', {
    'center': get_centers(data),
    'factor_depth': get_factor_depth(),
    'intrinsic_matrix': get_intrinsic_matrix(camera_data)
  })

  print(sio.whosmat('test.mat'))