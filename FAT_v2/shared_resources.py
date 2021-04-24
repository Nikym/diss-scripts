import os
import json

ROOT_DIR = '/media/nikita/Samsung_T5/diss/fat/'
OUT_DIR = '/media/nikita/Samsung_T5/diss/fat/output/'

DIRS = [
    'kitchen_0', 'kitchen_1', 'kitchen_2', 'kitchen_3', 'kitchen_4',
    'kitedemo_0', 'kitedemo_1', 'kitedemo_2', 'kitedemo_3', 'kitedemo_4',
    'temple_0', 'temple_1', 'temple_2', 'temple_3', 'temple_4'
]

NUM_SETS = len(DIRS)

def process_mixed(func) -> int:
    '''
    Process the directory structure of the mixed sets of scenes.
    '''
    MIXED_DIR = ROOT_DIR + 'mixed/'
    template = '{root}{dir1}/'
    print('Processing mixed instance directory...')

    id_track = 0
    for i, _dir in enumerate(DIRS):
        id_track = i * 4000
        padded_dir = str(i).zfill(2)
        ac_dir = _dir
        print('    - Looking at set ' + ac_dir + ' ')
        try:
            os.mkdir(OUT_DIR + padded_dir)
        except Exception:
            print('    (Directory "processed/' + padded_dir + '" already created, skipping creation...)')

        scene_dir = template.format(
            root=MIXED_DIR, dir1=ac_dir
        )
        for _id in range(0, 4000):
            if (_id % 200 == 0):
                print('        -> ' + str(_id))
            if _id >= 2000:
                angle = 'right'
            else:
                angle = 'left'

            ac_id = _id % 2000
            scene_id = str(ac_id).zfill(6) + '.' + angle
            new_id = str(_id + id_track).zfill(6)

            func(scene_dir, scene_id, OUT_DIR + padded_dir + '/', new_id)
        print('        -> done!')

    return id_track

def process_single(id_track: int, func):
    '''
    Process the directory structure of the single sets of scenes.
    '''
    SINGLE_DIR = ROOT_DIR + 'single/'
    template = '{root}{object}/{dir2}/'
    print('Processing single instance directory...')

    with open('/home/nikita/diss/scripts/objects.json') as f:
        objects = json.load(f)['objects']

    for i, obj in enumerate(objects):
        obj = obj + '_16k'
        padded_dir = str(i + NUM_SETS).zfill(2)
        print('    - Looking at object ' + obj + ' ')
        try:
            os.mkdir(OUT_DIR + padded_dir)
        except Exception:
            print('    (Directory "processed/' + padded_dir + '" already created, skipping creation...)')

        for _dir in DIRS:
            scene_dir = template.format(
                root=SINGLE_DIR, object=obj, dir2=_dir
            )
            print('        -> ' + _dir)
            for _id in range(0, 200):
                if _id >= 100:
                    angle = 'right'
                else:
                    angle = 'left'

                ac_id = _id % 100
                scene_id = str(ac_id).zfill(6) + '.' + angle
                new_id = str(_id + id_track).zfill(6)

                func(scene_dir, scene_id, OUT_DIR + padded_dir + '/', new_id)
            id_track += 200
        print('        -> done!')