import cv2
import json
import os
import numpy as np
from common_funcs import ROOT_PATH

OUTPUT_PATH = ROOT_PATH + '/output/img'

def change_pixel_value(path: str, frm: int, to: int):
  img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  img[np.where(img == [frm])] = [to]
  
  cv2.imwrite(path, img)

def get_object_names(path: str):
  names = []
  with open(path) as f:
    while True:
      line = f.readline()
      if not line:
        break
        
      names.append(line.split(' ')[0])
  
  return names

def is_single_object(path: str):
  with open(path) as f:
    count = sum(1 for _ in f)
    if count is 1:
      return True
  return False

def get_conversion_list() -> dict:
  with open(ROOT_PATH + '/output/object_ids.json', 'r') as f:
    return json.load(f)

if __name__ == '__main__':
  print('Adjusting segmentation IDs in label images...')
  ids = get_conversion_list()

  count = len([1 for x in list(os.scandir(ROOT_PATH + "/output/box")) if x.is_file()])

  for scene_id in range(count):
    full_id = str(scene_id).zfill(6)
    box_path = ROOT_PATH + '/output/box/' + full_id + '-box.txt'

    if is_single_object(box_path):
      print(ids[get_object_names(box_path)])
      # change_pixel_value(
      #   OUTPUT_PATH + '/' + full_id + '-label.png',
      #   frm=255,
      #   to=ids[get_object_names(box_path)]
      # )

    # for name in files:
    #   if is_single_object(os.path.join(root, name)):
    #     img_id = name[:-7] + 'label.png'
    #     print(img_id)