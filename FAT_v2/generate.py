import scipy.io as sio
import numpy as np

ROOT_LOV_PATH = '/home/nikita/diss/PoseCNN/data/LOV'

def filter_file(file_name: str):
	print('Processing {} file ...'.format(file_name))
	with open('/home/nikita/diss/scripts/outputs/{}.txt'.format(file_name), 'r') as og_file:
		with open('/home/nikita/diss/scripts/outputs/{}_formatted.txt'.format(file_name), 'w') as new_file:
			dir = ''
			for line in og_file:
				if line[:3] != dir:
					dir = line[:3]
					print('Looking at ' + dir + ' files ...')
				file_name = line[:-1]
				mat = sio.loadmat(ROOT_LOV_PATH + '/data/' + file_name + '-meta.mat')
				cls_indexes = mat['cls_indexes'].flatten()

				if len(np.unique(cls_indexes)) == len(cls_indexes):
					if len(mat['poses']) != 0:
						new_file.write(line)

ROOT_PATH = '/media/nikita/Samsung_T5/diss/fat/output/'
OUT_PATH = '/home/nikita/diss/scripts/outputs'

NUM_DIRS = 36
TEST_PERCENTAGE = 20

# NUM_VAL_DIRS = int((NUM_DIRS / 100) * TEST_PERCENTAGE)
# print(NUM_VAL_DIRS)

VALIDATE_DIRS = [0,1,5,6,10,11]

print('Creating list.txt ...')
with open(OUT_PATH + '/list.txt', 'w') as train_file:
	for n in range(0, NUM_DIRS):
		# if n in VALIDATE_DIRS:
		# 	continue

		padded_dir = str(n).zfill(2)
		if n < 15:
			for i in range(0, 4000):
				scene_id = str(i + n*4000).zfill(6)
				train_file.write(padded_dir + '/' + scene_id + '\n')
		else:
			for i in range(0, 3000):
				scene_id = str(i + 14*4000 + (n-15)*3000).zfill(6)
				train_file.write(padded_dir + '/' + scene_id + '\n')

# print('Creating val.txt ...')
# with open(OUT_PATH + '/val.txt', 'w') as val_file:
# 	for n in VALIDATE_DIRS:
# 		padded_dir = str(n).zfill(2)
# 		for i in range(0, 4000):
# 			scene_id = str(i + n*4000).zfill(6)
# 			val_file.write(padded_dir + '/' + scene_id + '\n')

filter_file('list')

print('Creating train.txt and val.txt ...')
with open(OUT_PATH + '/train.txt', 'w') as train_file:
	with open(OUT_PATH + '/val.txt', 'w') as val_file:
		with open(OUT_PATH + '/list_formatted.txt', 'r') as list_file:
			for i, scene in enumerate(list_file.readlines()):
				if i % 10 == 0 or i % 10 == 1:
					val_file.write(scene)
				else:
					train_file.write(scene)

print('Done')