import sys

ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:

    sys.path.remove(ros_path)

import cv2

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

import json
import os
import numpy as np
from common_funcs import ROOT_PATH

OUTPUT_PATH = ROOT_PATH + '/output/img'

def change_pixel_value(path: str, frm: int, to: int):
  '''
  Adjusts specified pixel value to new value.

    Parameters:
      path (str) - Path to img
      from (int) - Pixel value (0-255)
      to (int) - Pixel value (0-255)
  '''
  img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  img[np.where(img == [frm])] = [to]
  
  cv2.imwrite(path, img)

def get_object_names(path: str) -> list:
  '''
  Retrives names of objects present in file.

    Parameters:
      path (str) - Path to img
    
    Returns:
      names (list) - List of object names
  '''
  names = []
  with open(path) as f:
    while True:
      line = f.readline()
      if not line:
        break
        
      names.append(line.split(' ')[0])
  
  return names

def is_single_object(path: str) -> bool:
  '''
  Checks if specified file contains only one object.

    Parameters:
      path (str) - Path to box file

    Returns:
      is_single (bool) - Boolean true or false
  '''
  with open(path) as f:
    count = sum(1 for _ in f)
    if count is 1:
      return True
  return False

def create_new_ids_dict(object_ids: dict) -> dict:
  '''
  Creates new updates IDs for objects.

    Parameters:
      object_ids (dict) - Dictionary of object : ID pairs
    
    Returns:
      new_object_ids (dict) - Dictionary of new n object IDs ranging from 0 to n
  '''
  new_object_ids = {}
  
  objects = sorted(object_ids.keys())
  
  for i, obj in enumerate(objects):
    new_object_ids[obj] = i+1

  return new_object_ids

def get_conversion_list() -> dict:
  '''
  Get hash table of object segmentation IDs.

    Returns:
      object_ids (dict) - Hash table of object-id pairs
  '''
  with open(ROOT_PATH + '/output/object_ids.json', 'r') as f:
    return json.load(f)

def convert_to_new_ids(path: str, obj_names: list, old_ids: dict, new_ids: dict):
  '''
  Converts old IDs to new IDs.
  '''
  for obj_name in obj_names:
    old_id = old_ids[obj_name]
    new_id = new_ids[obj_name]

    change_pixel_value(path, old_id, new_id)

if __name__ == '__main__':
  print('Adjusting segmentation IDs in label images...')
  ids = get_conversion_list()
  new_ids = create_new_ids_dict(ids)

  count = len([1 for x in list(os.scandir(ROOT_PATH + "/output/box")) if x.is_file()])

  log_file = open(ROOT_PATH + '/output/img_seg_adjust_log.txt', 'w')

  for scene_id in range(count):
    full_id = str(scene_id).zfill(6)
    if scene_id % 200 == 0:
      print('@ scene {}'.format(full_id))

    box_path = ROOT_PATH + '/output/box/' + full_id + '-box.txt'

    objs = get_object_names(box_path)
    if is_single_object(box_path):
      log_file.write(
        full_id + '-label.png: 255 ->' + str(ids[objs[0]]) + '\n'
      )
      change_pixel_value(
        OUTPUT_PATH + '/' + full_id + '-label.png',
        frm=255,
        to=ids[objs[0]]
      )
    
    convert_to_new_ids(
      OUTPUT_PATH + '/' + full_id + '-label.png',
      objs,
      ids,
      new_ids
    )
  
  with open(ROOT_PATH + '/output/new_object_ids.json', 'w+') as f:
    f.write(json.dumps(new_ids, indent=2))
  
  log_file.close()
  print('Complete')
