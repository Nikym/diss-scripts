import scipy.io as sio
import numpy as np
import json
import os

ROOT_PATH = '/Volumes/nik_ext/diss/fat_dataset/fat'

def getCenters(data: dict) -> np.ndarray:
  n = len(data['objects'])
  centers = np.empty((n, 2), dtype=np.float32)

  for i, obj in enumerate(data['objects']):
    print(np.array(obj['projected_cuboid_centroid'], dtype=np.float32))
    centers[i] = obj['projected_cuboid_centroid']

  return centers

if __name__ == '__main__':
  print('Creating .mat files...')

  with open(ROOT_PATH + '/mixed/kitchen_0/000000.right.json') as f:
    data = json.load(f)

  sio.savemat('test.mat', {
    'center': getCenters(data)
  })

  print(sio.whosmat('test.mat'))