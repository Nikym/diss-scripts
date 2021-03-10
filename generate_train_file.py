import os
from collections import defaultdict

ROOT_PATH = '/media/external/diss/fat_dataset/far/output/combined'
POSECNN_PATH = '~/diss/PoseCNN/data/LOV'

# Retrieve the number of files in each folder
file_count = defaultdict(int)
dirs = next(os.walk(ROOT_PATH))[1]
for directory in dirs:
  file_count[directory] = len(next(os.walk(ROOT_PATH + '/' + directory))[2])

# Create new train file with the relative paths of data
with open(POSECNN_PATH + '/train_new.txt', 'w') as train_file:
  for n in len(file_count.keys()):
    for scene_id in range(file_count[str(n+1).zfill(3)]):
      train_file.write(directory + '/' + str(scene_id + n*1200).zfill(6) + '\n')