import os
from collections import defaultdict

ROOT_PATH = '/media/external/diss/fat_dataset/fat/output/combined'
POSECNN_PATH = '/home/nikita/diss/PoseCNN/data/LOV'

# Retrieve the number of files in each folder
file_count = defaultdict(int)
dirs = [d for d in os.listdir(ROOT_PATH) if os.path.isdir(d)]
for directory in dirs:
  file_count[directory] = len([f for f in os.listdir(ROOT_PATH + '/' + directory) if os.path.isfile(f)])

# Create new train file with the relative paths of data
with open(POSECNN_PATH + '/train_new.txt', 'w') as train_file:
  for n in range(len(file_count.keys())):
    for scene_id in range(file_count[str(n+1).zfill(3)]):
      train_file.write(directory + '/' + str(scene_id + n*1200).zfill(6) + '\n')