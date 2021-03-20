import scipy.io as sio
import json
import os
from common_funcs import ROOT_PATH

MAT_ROOT = ROOT_PATH + '/output/mat'

count = len([1 for x in list(os.scandir(MAT_ROOT)) if x.is_file()])

for x in range(count):
  scene_id = str(x).zfill(6)
  mat_path = MAT_ROOT + '/' + scene_id + '-meta.mat'

  if x % 2000 == 0:
    print('At ' + scene_id + ' ...')

  data = sio.loadmat(mat_path)
  
  for i in range(len(data['center'])):
    data['center'][i][0] -= 160
    data['center'][i][1] -= 30

  sio.savemat(mat_path, data)

print('Complete!')
    