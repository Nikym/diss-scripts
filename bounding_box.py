import json
import os

ROOT_PATH = '/home/nikita/diss/fat_dataset/fat'
FAILED_FILES = []

def get_failed_files():
  with open(ROOT_PATH + '/img_processing_err.txt', 'r') as err_file:
    while True:
      f = err_file.readline()
      if not f:
        break

      FAILED_FILES.append(f)

def processScenes(path: str, start_index: int, output_dir: str) -> int:
  '''
  Processes the json files in a specified directory and outputs bounding box text files.

    Parameters:
      path (str): The path of the directory to be processed
      start_index (int): The index at which the output file names should start at
      output_dir (str): The path to the output directory

    Returns:
      num_files_processed (int): The number of files that were processed
  '''
  # Each scene has 2 angles with 4 data files each, plus 2 camera files not related (hence -2)
  num_of_files = int((len(os.listdir(path)) - 2) / 8)

  index = 0
  for x in range(0, num_of_files):
    # There are right and left angles, so can split them into seperate files
    for angle in ['left', 'right']:
      file_name = str(x).zfill(6) + '.' + angle + '.json'
      meta_file = open(os.path.join(path, file_name))

      data = json.load(meta_file)
      new_file = open(
        os.path.join(output_dir, str(index + start_index).zfill(6) + '-box.txt'), 'w+')

      # Iterate for each object in scene and get names and bounding box coords
      for obj in data['objects']:
        name = obj['class']
        name = name[:-4]

        box = obj['bounding_box']
        tl_coords = str(
          round(box['top_left'][0], 2)) + ' ' + str(round(box['top_left'][1], 2))
        br_coords = str(
          round(box['bottom_right'][0], 2)) + ' ' + str(round(box['bottom_right'][1], 2))

        obj_data = name + ' ' + tl_coords + ' ' + br_coords
        new_file.write(obj_data + '\n')
      
      meta_file.close()
      new_file.close()

  # Multiplied by 2 as each scene has two angles
  return num_of_files * 2

# Get names of directories at root
dir_list_mixed = [
  'mixed/' + item for item in os.listdir(ROOT_PATH + '/mixed') if os.path.isdir(os.path.join(ROOT_PATH, 'mixed', item))]
# Sorted to ensure processed data is always in same order
dir_list_mixed.sort()

dir_list_single_objs = [
  'single/' + item for item in os.listdir(ROOT_PATH + '/single') if os.path.isdir(os.path.join(ROOT_PATH, 'single', item))]

dir_list_single = []
for directory in dir_list_single_objs:
  dir_list_single.extend(
    [directory + '/' + item for item in os.listdir(ROOT_PATH + '/' + directory) if os.path.isdir(os.path.join(ROOT_PATH, directory, item))]
  )

dir_list_single.sort()

dir_list = []
dir_list.extend(dir_list_mixed)
dir_list.extend(dir_list_single)

log_file = open('data_processing_log.txt', 'w+')

total_files = 0
for directory in dir_list:
  path = ROOT_PATH + '/' + directory
  print('Processing ' + directory + ' ... (start @ ' + str(total_files) + ')')
  log_file.write('[' + str(total_files).zfill(5) + '] ' + directory + '\n')
  total_files += processScenes(path, total_files, 'output')

log_file.close()

print('Complete')