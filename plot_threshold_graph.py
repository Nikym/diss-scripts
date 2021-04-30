from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.io as sio
import argparse
import os, sys
from collections import defaultdict

ITEMS = [
  '002_master_chef_can',
  '003_cracker_box',
  '004_sugar_box',
  '005_tomato_soup_can',
  '006_mustard_bottle',
  '007_tuna_fish_can',
  '008_pudding_box',
  '009_gelatin_box',
  '010_potted_meat_can'
  '011_banana',
  '019_pitcher_base',
  '021_bleach_cleanser',
  '024_bowl',
  '025_mug',
  '035_power_drill',
  '036_wood_block',
  '037_scissors',
  '040_large_marker',
  '051_large_clamp',
  '052_extra_large_clamp',
  '061_foam_brick'
]

def parse_args():
  parser = argparse.ArgumentParser(description='Extract accuracy-threshold graphs from given data')

  parser.add_argument('--src', dest='src', help='Path to test log file', default=None, type=str)
  parser.add_argument('--obj', dest='obj', help='Name of object to show data for', default=None, type=str)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args

def show_graphs(rot_diff_arr, trans_diff_arr, rot_angle):
  fig, axis = plt.subplots(1,3)
  # Accuracy-RotationThreshold
  x1 = np.arange(0,200,1)
  y1 = np.zeros(200)
  # Accuracy-TranslationThreshold
  x2 = np.arange(0,0.1,0.0005)
  y2 = np.zeros(200)
  # Instances-RotationError
  x3 = np.arange(0,200,10)
  y3 = rot_angle

  # Accuracy-Rotation
  total_rot = len(rot_diff_arr)
  for x in x1:
    count = len([r for r in rot_diff_arr if r <= x])
    y1[x] = count / total_rot

  # Accuracy-Translation
  total_trans = len(trans_diff_arr)
  for i, x in enumerate(x2):
    count = len([t for t in trans_diff_arr if t <= x])
    y2[i] = count / total_trans

  axis[0].plot(x1, y1)
  axis[0].set_xlim(xmin=0.0, xmax=180.0)
  axis[0].set_ylim(ymin=0.0, ymax=1.0)
  axis[0].set_ylabel('accuracy')
  axis[0].set_xlabel('rotation angle threshold')

  axis[1].plot(x2, y2)
  axis[1].set_xlim(xmin=0.0, xmax=0.1)
  axis[1].set_ylim(ymin=0.0, ymax=1.0)
  axis[1].set_xlabel('translation threshold in meters')

  axis[2].bar(x3, y3, width=10, align='edge', edgecolor='#000000')
  axis[2].set_xlim(xmin=0.0, xmax=180)
  axis[2].set_ylabel('instances')
  axis[2].set_xlabel('rotation angle error')

  plt.show()

def main():
  args = parse_args()

  # fig, axis = plt.subplots(1,3)

  # # Accuracy-RotationThreshold
  # x1 = np.arange(0,200,1)
  # y1 = np.zeros(200)

  # # Accuracy-TranslationThreshold
  # x2 = np.arange(0,0.1,0.0005)
  # y2 = np.zeros(200)

  # # Instances-RotationError
  # x3 = np.arange(0,200,10)
  y3 = np.zeros(20)

  object_graphs = defaultdict(
    lambda: {'trans': [], 'rot': [], 'rot-angle': np.zeros(20), 'total': 0, 'missed': 0}
  )

  rot_diff_arr = []
  trans_diff_arr = []
  total_items = 0
  missed_items = 0
  with open(args.src) as f:
    _obj = None
    for i, line in enumerate(f.readlines()):
      if line[:-1] in ITEMS:
        _obj = line[:-1]

      if line[:16] == 'rotation error: ':
        index = int(float(line[16:-2]) // 10)
        if index == 18:
          y3[index-1] += 1
          if _obj in ITEMS:
            object_graphs[_obj]['rot-angle'][index-1] += 1
        else:
          y3[index] += 1
          if _obj in ITEMS:
            object_graphs[_obj]['rot-angle'][index] += 1
        rot_diff_arr.append(float(line[16:-2]))
        if _obj in ITEMS:
          object_graphs[_obj]['rot'].append(float(line[16:-2]))
      elif line[:19] == 'translation error: ':
        trans_diff_arr.append(float(line[19:-2]))
        if _obj in ITEMS:
          object_graphs[_obj]['trans'].append(float(line[19:-2]))
      else:
        line_split = line.split(' ')
        if line_split[0] in ITEMS:
          total_items += 1
          object_graphs[line_split[0]]['total'] += 1
          if float(line_split[1][:-2]) == 0.0:
            missed_items += 1
            object_graphs[line_split[0]]['missed'] += 1
            rot_diff_arr.append(200)
            trans_diff_arr.append(1)
            object_graphs[line_split[0]]['trans'].append(1)
            object_graphs[line_split[0]]['rot'].append(200)
  
  # # Accuracy-Rotation
  # total_rot = len(object_graphs['003_cracker_box']['rot'])
  # for x in x1:
  #   count = len([r for r in object_graphs['003_cracker_box']['rot'] if r <= x])
  #   y1[x] = count / total_rot

  # # Accuracy-Rotation
  # total_rot = len(rot_diff_arr)
  # for x in x1:
  #   count = len([r for r in rot_diff_arr if r <= x])
  #   y1[x] = count / total_rot

  # # Accuracy-Translation
  # total_trans = len(object_graphs['003_cracker_box']['trans'])
  # for i, x in enumerate(x2):
  #   count = len([t for t in object_graphs['003_cracker_box']['trans'] if t <= x])
  #   y2[i] = count / total_trans

  # # Accuracy-Translation
  # total_trans = len(trans_diff_arr)
  # for i, x in enumerate(x2):
  #   count = len([t for t in trans_diff_arr if t <= x])
  #   y2[i] = count / total_trans

  # axis[0].plot(x1, y1)
  # axis[0].set_xlim(xmin=0.0, xmax=180.0)
  # axis[0].set_ylim(ymin=0.0, ymax=1.0)
  # axis[0].set_ylabel('accuracy')
  # axis[0].set_xlabel('rotation angle threshold')

  # axis[1].plot(x2, y2)
  # axis[1].set_xlim(xmin=0.0, xmax=0.1)
  # axis[1].set_ylim(ymin=0.0, ymax=1.0)
  # axis[1].set_xlabel('translation threshold in meters')

  # axis[2].bar(x3, y3, width=10, align='edge', edgecolor='#000000')
  # axis[2].set_xlim(xmin=0.0, xmax=180)
  # axis[2].set_ylabel('instances')
  # axis[2].set_xlabel('rotation angle error')

  # plt.show()
  if (args.obj in ITEMS):
    print(object_graphs[args.obj]['total'], object_graphs[args.obj]['missed'])
    print('missed: {}%'.format(round(float((object_graphs[args.obj]['missed'] / object_graphs[args.obj]['total'])) * 100, 2)))
    show_graphs(object_graphs[args.obj]['rot'], object_graphs[args.obj]['trans'], object_graphs[args.obj]['rot-angle'])
  else:
    print(total_items, missed_items)
    print('missed: {}%'.format(round(float((missed_items / total_items)) * 100, 2)))
    show_graphs(rot_diff_arr, trans_diff_arr, y3)

if __name__ == '__main__':
  main()