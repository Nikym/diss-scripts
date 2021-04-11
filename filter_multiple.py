import scipy.io as sio
import numpy as np

ROOT_PATH = '/home/nikita/diss/PoseCNN/data/LOV'

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
				mat = sio.loadmat(ROOT_PATH + '/data/' + file_name + '-meta.mat')
				cls_indexes = mat['cls_indexes'].flatten()

				if len(np.unique(cls_indexes)) == len(cls_indexes):
					if len(mat['poses']) != 0:
						new_file.write(line)

filter_file('train')
filter_file('val')

print('done')

