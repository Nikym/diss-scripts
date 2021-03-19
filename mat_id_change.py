import scipy.io as sio
import json
import os
from common_funcs import ROOT_PATH

MAT_ROOT = ROOT_PATH + '/output/mat'

with open(ROOT_PATH + '/output/object_ids.json') as f:
  old_ids = json.load(f)

old_ids = {value: key for key, value in old_ids.items()}

print(old_ids)

with open(ROOT_PATH + '/output/new_object_ids.json') as f:
  new_ids = json.load(f)

count = len([1 for x in list(os.scandir(MAT_ROOT)) if x.is_file()])

# for x in range(count):
#   scene_id = str(x).zfill(6)
#   mat_path = MAT_ROOT + '/' + scene_id + '-meta.mat'

#   data = sio.loadmat(mat_path)
  
#   for i in len(data['cls_indexes']):
    