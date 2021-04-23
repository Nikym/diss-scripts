import os
import json

ROOT_DIR = '/media/nikita/Samsung_T5/diss/generated_data/100k/'
OUT_DIR = '/media/nikita/Samsung_T5/diss/generated_data/processed/'
NUM_SETS = 29

def process_mixed(func) -> int:
    '''
    Process the directory structure of the mixed sets of scenes.
    '''
    MIXED_DIR = ROOT_DIR + 'mixed/'
    template = '{root}{dir1}/{dir2}/'
    print('Processing mixed instance directory...')

    id_track = 0
    for _dir in range(0, NUM_SETS):
        # id_track = _dir * 2000 + 102000
        id_track = _dir * 2000
        padded_dir = str(_dir).zfill(2)
        ac_dir = str(_dir).zfill(2)
        print('    - Looking at set ' + padded_dir + ' ')
        try:
            os.mkdir(OUT_DIR + padded_dir)
        except Exception:
            print('    (Directory "processed/' + padded_dir + '" already created, skipping creation...)')

        for _set in range(0, 10):
            print('        -> ' + str(_set).zfill(2))
            scene_dir = template.format(
                root=MIXED_DIR, dir1=ac_dir, dir2=_set
            )
            for _id in range(0, 200):
                scene_id = str(_id).zfill(6)
                new_id = str(_id + id_track).zfill(6)

                func(scene_dir, scene_id, OUT_DIR + padded_dir + '/', new_id)
            id_track += 200
        print('        -> done!')

    return id_track

def process_single(id_track: int, func):
    '''
    Process the directory structure of the single sets of scenes.
    '''
    SINGLE_DIR = ROOT_DIR + 'single/'
    template = '{root}{object}/'
    print('Processing single instance directory...')

    with open('/home/nikita/diss/scripts/objects.json') as f:
        objects = json.load(f)['objects']

    for i, obj in enumerate(objects):
        padded_dir = str(i + NUM_SETS).zfill(2)
        print('    - Looking at object ' + obj + ' ')
        try:
            os.mkdir(OUT_DIR + padded_dir)
        except Exception:
            print('    (Directory "processed/' + padded_dir + '" already created, skipping creation...)')

        scene_dir = template.format(
            root=SINGLE_DIR, object=obj
        )
        for _id in range(0, 2000):
            if (_id % 200 == 0):
                print('        -> ' + str(_id))
            scene_id = str(_id).zfill(6)
            new_id = str(_id + id_track).zfill(6)

            func(scene_dir, scene_id, OUT_DIR + padded_dir + '/', new_id)
        id_track += 2000
        print('        -> done!')