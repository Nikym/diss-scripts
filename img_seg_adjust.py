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

def is_single_object(path: str):
  with open(path) as f:
    count = sum(1 for _ in f)
    if count is 1:
      return True
  return False

def get_conversion_list() -> dict:
  with open(ROOT_PATH + '/output/object_ids..json', 'r') as f:
    return json.load(f)

if __name__ == '__main__':
  print('Adjusting segmentation IDs in label images...')
  ids = get_conversion_list()

  for path in os.walk(ROOT_PATH + '/output/box'):
    if is_single_object(path):
      img_id = path[-14:-7] + 'label.png'
      print(img_id)