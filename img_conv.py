import cv2
import os
from fat_to_ycb_meta import get_directories

ROOT_PATH = '/media/external/diss/fat_dataset/fat'

def crop_image(img):
  cropped = img[30:30+480, 160:160+640]

  return cropped

def process_scenes(path: str, start_index: int, output_dir: str = 'output') -> int:
  '''
  Processes the image files in a specified directory and outputs image files.

    Parameters:
      path (str): The path of the directory to be processed
      start_index (int): The index at which the output file names should start at
      output_dir (str): The path to the output directory

    Returns:
      num_files_processed (int): The number of files that were processed
  '''
  # Each scene has 2 angles with 4 data files each, plus 2 camera / obj files not related
  num_of_files = int((len(os.listdir(path)) - 2) / 8)

  err_file = open(ROOT_PATH + '/img_processing_err.txt', 'a')

  index = 0
  for x in range(0, num_of_files):
    for angle in ['left', 'right']:
      file_path = os.path.join(path, str(x).zfill(6) + '.' + angle)

      # If any of the img files are corrupt, then skip whole instance
      try:
        file_name = file_path + '.jpg'
        cropped_img = crop_image(cv2.imread(file_name))

        depth_file_name = file_path + '.depth.png'
        cropped_depth = crop_image(cv2.imread(depth_file_name))

        seg_file_name = file_path + '.seg.png'
        cropped_seg = crop_image(cv2.imread(seg_file_name))

        new_file_id = output_dir + '/' + str(index + start_index).zfill(6)

        cv2.imwrite(new_file_id + '-color.png', cropped_img)
        cv2.imwrite(new_file_id + '-depth.png', cropped_depth)
        cv2.imwrite(new_file_id + '-label.png', cropped_seg)
        index += 1
      except Exception:
        print('Error! File affected ' + file_path)
        err_file.write(file_path + '/n')
  
  err_file.close()

  return index

if __name__ == '__main__':
  print('Cropping colour and depth images...')

  dir_list = get_directories(ROOT_PATH + '/')

  log_file = open(ROOT_PATH + '/img_processing_log.txt', 'w')

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
      ROOT_PATH + '/output_img'
    )
  
  log_file.close()