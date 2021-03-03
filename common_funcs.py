import os

ROOT_PATH = '/media/external/diss/fat_dataset/fat'

def get_failed_files() -> list:
  '''
  Reads list of corrupted files and loads them into a list.

    Returns:
      failed_files (list): String list of corrupted files
  '''
  failed_files = []
  with open(ROOT_PATH + '/output/img_processing_err.txt', 'r') as err_file:
    while True:
      f = err_file.readline()
      if not f:
        break

      failed_files.append(f)

  return failed_files

def get_directories(root: str = '') -> list:
  '''
  Retrives relative paths to the FAT files.

    Parameters:
      root (str): The root directory of the FAT dataset

    Returns:
      dir_list (list): List of relative paths
  '''

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

  return dir_list