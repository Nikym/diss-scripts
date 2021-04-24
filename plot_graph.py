from matplotlib import pyplot as plt
import numpy as np
import math
import csv
import argparse
import os, sys

STEP_SIZE = 200
ITERS = 160000
SMOOTH = 100

def parse_args():
  parser = argparse.ArgumentParser(description='Extract error graphs from log files')
  
  parser.add_argument('--csv', dest='csv_file', help='Path to CSV file', default=None, type=str)
  parser.add_argument('--title', dest='title', help='Title of the figure', default='', type=str)
  parser.add_argument('--smooth', dest='smooth_size', help='X-axis smoothing size', default=100, type=int)
  parser.add_argument('--iters', dest='iter_size', help='Number of iterations completed', default=160000, type=int)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args

def smooth(arr: np.array) -> np.array:
  smooth_arr = []
  for i in range(0, len(arr), SMOOTH):
    _sum = 0
    for j in range(0, SMOOTH):
      try:
        _sum += arr[i+j]
      except Exception:
        break
    smooth_arr.append(_sum/SMOOTH)
  
  return np.array(smooth_arr)

def normalise(arr: np.array) -> np.array:
  norm_array = []
  diff_arr = max(arr) - min(arr)
  for i in arr:
    temp = (((i - min(arr))*1)/diff_arr)
    norm_array.append(temp)

  return np.array(norm_array)

def main():
  args = parse_args()
  ITERS = args.iter_size

  fig, axis = plt.subplots(2,2)
  fig.suptitle(args.title)

  x = np.arange(0, ITERS, SMOOTH)
  y1 = np.zeros(ITERS)
  y2 = np.zeros(ITERS)
  y3 = np.zeros(ITERS)
  y4 = np.zeros(ITERS)

  with open(args.csv_file) as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
      if i == 0:
        continue
      if i-1 == ITERS:
        break
      y1[(i-1)] = row[0]
      y2[(i-1)] = row[1]
      y3[(i-1)] = row[2]
      y4[(i-1)] = row[3]

  y1 = smooth(y1)
  axis[0,0].plot(x, y1)
  axis[0,0].plot(x, np.poly1d(np.polyfit(x, y1, 1))(x), c='#ff7f0e')
  axis[0,0].set_title('loss')
  axis[0,0].set_ylabel('loss')

  y2 = smooth(y2)
  axis[0,1].plot(x, y2, label='loss value')
  axis[0,1].plot(x, np.poly1d(np.polyfit(x, y2, 1))(x), c='#ff7f0e', label='trend')
  axis[0,1].set_title('loss_cls')

  y3 = smooth(y3)
  axis[1,0].plot(x, y3)
  axis[1,0].plot(x, np.poly1d(np.polyfit(x, y3, 1))(x), c='#ff7f0e')
  axis[1,0].set_title('loss_vertex')
  axis[1,0].set_xlabel('iterations')
  axis[1,0].set_ylabel('loss')

  y4 = smooth(y4)
  axis[1,1].plot(x, y4)
  axis[1,1].plot(x, np.poly1d(np.polyfit(x, y4, 1))(x), c='#ff7f0e')
  axis[1,1].set_title('loss_pose')
  axis[1,1].set_xlabel('iterations')

  axis[0,1].legend()

  plt.show()

if __name__ == '__main__':
  main()