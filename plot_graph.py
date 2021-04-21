from matplotlib import pyplot as plt
import numpy as np
import math
import csv
import argparse
import os, sys

STEP_SIZE = 200

def parse_args():
  parser = argparse.ArgumentParser(description='Extract error graphs from log files')
  
  parser.add_argument('--csv', dest='csv_file', help='Path to CSV file', default=None, type=str)
  parser.add_argument('--step', dest='step_size', help='X-axis step size', default=200, type=int)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args

def normalise(arr: np.array) -> np.array:
  norm_array = []
  diff_arr = max(arr) - min(arr)
  for i in arr:
    temp = (((i - min(arr))*1)/diff_arr)
    norm_array.append(temp)

  return np.array(norm_array)

def main():
  args = parse_args()
  _, axis = plt.subplots(2,2)

  x = np.arange(0, 160000, args.step_size)
  y1 = np.zeros(160000 // args.step_size)
  y2 = np.zeros(160000 // args.step_size)
  y3 = np.zeros(160000 // args.step_size)
  y4 = np.zeros(160000 // args.step_size)

  with open(args.csv_file) as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
      if i == 0:
        continue
      if (i-1) % args.step_size == 0:
        y1[(i-1) // args.step_size] = row[0]
        y2[(i-1) // args.step_size] = row[1]
        y3[(i-1) // args.step_size] = row[2]
        y4[(i-1) // args.step_size] = row[3]

  y1 = normalise(y1)
  axis[0,0].plot(x, y1)
  axis[0,0].plot(x, np.poly1d(np.polyfit(x, y1, 1))(x))
  axis[0,0].set_title('loss')

  y2 = normalise(y2)
  axis[0,1].plot(x, y2)
  axis[0,1].plot(x, np.poly1d(np.polyfit(x, y2, 1))(x))
  axis[0,1].set_title('loss_cls')

  y3 = normalise(y3)
  axis[1,0].plot(x, y3)
  axis[1,0].plot(x, np.poly1d(np.polyfit(x, y3, 1))(x))
  axis[1,0].set_title('loss_vertex')

  y4 = normalise(y4)
  axis[1,1].plot(x, y4)
  axis[1,1].plot(x, np.poly1d(np.polyfit(x, y4, 1))(x))
  axis[1,1].set_title('loss_pose')

  plt.show()

if __name__ == '__main__':
  main()