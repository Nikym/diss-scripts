ROOT_PATH = '/media/nikita/Samsung_T5/diss/fat/output/'
OUT_PATH = '/home/nikita/diss/scripts/outputs'

NUM_DIRS = 35
TEST_PERCENTAGE = 20

# NUM_VAL_DIRS = int((NUM_DIRS / 100) * TEST_PERCENTAGE)
# print(NUM_VAL_DIRS)

VALIDATE_DIRS = [0,1,5,6,10,11]

print('Creating train.txt ...')
with open(OUT_PATH + '/train.txt', 'w') as train_file:
	for n in range(0, NUM_DIRS):
		if n in VALIDATE_DIRS:
			continue

		padded_dir = str(n).zfill(2)
		if n < 15:
			for i in range(0, 4000):
				scene_id = str(i + n*4000).zfill(6)
				train_file.write(padded_dir + '/' + scene_id + '\n')
		else:
			for i in range(0, 3000):
				scene_id = str(i + 14*4000 + (n-15)*3000).zfill(6)
				train_file.write(padded_dir + '/' + scene_id + '\n')

print('Creating val.txt ...')
with open(OUT_PATH + '/val.txt', 'w') as val_file:
	for n in VALIDATE_DIRS:
		padded_dir = str(n).zfill(2)
		for i in range(0, 2000):
			scene_id = str(i + n*2000).zfill(6)
			val_file.write(padded_dir + '/' + scene_id + '\n')

print('Done')