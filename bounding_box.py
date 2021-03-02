import json
import os
from fat_to_ycb_meta import get_directories

ROOT_PATH = '/home/nikita/diss/fat_dataset/fat'
FAILED_FILES = []

def get_failed_files():
  '''
  Reads list of corrupted files and loads them into a list.
  '''
  with open(ROOT_PATH + '/img_processing_err.txt', 'r') as err_file:
    while True:
      f = err_file.readline()
      if not f:
        break

      FAILED_FILES.append(f)

def process_scenes(path: str, start_index: int, output_dir: str) -> int:
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
      
      # If file does not have processed image then skip
      if os.path.join(path, file_name[0:-5]) in FAILED_FILES:
        continue

      meta_file = open(os.path.join(path, file_name))

      data = json.load(meta_file)
      new_file = open(
        os.path.join(output_dir, str(index + start_index).zfill(6) + '-box.txt'), 'w')

      # Iterate for each object in scene and get names and bounding box coords
      for obj in data['objects']:
        name = obj['class']
        name = name[:-4]

        box = obj['bounding_box']
        tl_x_coord = round(box['top_left'][0], 2)
        if tl_x_coord > 640:
          continue # If start is beyond boundary then item is not in frame
        elif tl_x_coord < 0:
          tl_x_coord = 0.0

        tl_y_coord = round(box['top_left'][1], 2)
        if tl_y_coord > 480:
          continue
        elif tl_y_coord < 0:
          tl_y_coord = 0.0

        tl_coords = str(tl_x_coord) + ' ' + str(tl_y_coord)  

        br_x_coord = round(box['bottom_right'][0], 2)
        if br_x_coord < 0:
          continue # If end is before boundary then item is not in frame
        elif br_x_coord > 640:
          br_x_coord = 640.0
        
        br_y_coord = round(box['bottom_right'][1], 2)
        if br_y_coord < 0:
          continue
        elif br_y_coord > 480:
          br_y_coord = 480.0

        br_coords = str(br_x_coord) + ' ' + str(br_y_coord)

        obj_data = name + ' ' + tl_coords + ' ' + br_coords
        new_file.write(obj_data + '\n')
      
      meta_file.close()
      new_file.close()
      index += 1

  # Multiplied by 2 as each scene has two angles
  return index

if __name__ == '__main__':
  print('Creating bounding box txt files...')
  get_failed_files()

  dir_list = get_directories(ROOT_PATH + '/')

  log_file = open(ROOT_PATH + '/box_processing_log.txt', 'w')

  total_files = 0
  total_dir = len(dir_list)

  log_file.write('Total directories: ' + str(total_dir) + '\n')

  for i, directory in enumerate(dir_list):
    print('Processing ' + directory + ' ... (start @ ' + 
      str(total_files) + ', dir ' + str(i+1) + '/' + str(total_dir) + ')')
    log_file.write('[' + str(total_files).zfill(5) + '] ' + directory + '\n')

    path = ROOT_PATH + '/' + directory
    total_files += process_scenes(
      path,
      total_files,
      ROOT_PATH + '/output_box'
    )

  log_file.close()
  print('Complete')