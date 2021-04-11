ROOT_PATH = '/media/nikita/Samsung_T5/diss/generated_data/processed/'
OUT_PATH = '/home/nikita/diss/scripts/outputs'

# 62 normally
NUM_DIRS = 80
TEST_PERCENTAGE = 20

NUM_VAL_DIRS = int((NUM_DIRS / 100) * TEST_PERCENTAGE)
print(NUM_VAL_DIRS)

print('Creating train.txt ...')
with open(OUT_PATH + '/train.txt', 'w') as train_file:
	for n in range(0, NUM_DIRS - NUM_VAL_DIRS):
		padded_dir = str(n).zfill(2)
		for i in range(0, 2000):
			scene_id = str(i + n*2000).zfill(6)
			train_file.write(padded_dir + '/' + scene_id + '\n')

print('Creating val.txt ...')
with open(OUT_PATH + '/val.txt', 'w') as val_file:
	for n in range(NUM_DIRS - NUM_VAL_DIRS, NUM_DIRS):
		padded_dir = str(n).zfill(2)
		for i in range(0, 2000):
			scene_id = str(i + n*2000).zfill(6)
			val_file.write(padded_dir + '/' + scene_id + '\n')

print('Done')
