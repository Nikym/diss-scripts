import json
import os
from shared_resources import ROOT_DIR, OUT_DIR, NUM_SETS, process_mixed, process_single

def create_bounding_box(scene_path: str, scene_id: str, out_path: str, new_id: str):
    '''
    Create bounding box file for given scene.

        Parameters:
            scene_path (str): Path to the original scene directory
            scene_id (str): ID of the scene
            out_path (str): Path to the output directory
            new_id (str): New synchronised ID of scene
    '''
    with open(scene_path + scene_id + '.json') as f:
        scene_data = json.load(f)

    box_file = open(out_path + new_id + '-box.txt', 'w')
    
    for obj in scene_data['objects']:
        name = obj['class']
        box = obj['bounding_box']

        tl_x_coord = round(box['top_left'][1], 2)
        if tl_x_coord > 640:
            continue # Out of frame
        elif tl_x_coord < 0:
            tl_x_coord = 0.0

        tl_y_coord = round(box['top_left'][0], 2)
        if tl_y_coord > 480:
            continue
        elif tl_y_coord < 0:
            tl_y_coord = 0.0

        tl_coords = str(tl_x_coord) + ' ' + str(tl_y_coord)

        br_x_coord = round(box['bottom_right'][1], 2)
        if br_x_coord < 0:
            continue # If end is before boundary then item is not in frame
        elif br_x_coord > 640:
            br_x_coord = 640.0

        br_y_coord = round(box['bottom_right'][0], 2)
        if br_y_coord < 0:
            continue
        elif br_y_coord > 480:
            br_y_coord = 480.0

        br_coords = str(br_x_coord) + ' ' + str(br_y_coord)
        obj_data = name + ' ' + tl_coords + ' ' + br_coords
        box_file.write(obj_data + '\n')
    
    box_file.close()

def main():
    print('*** BEGINNING BOUNDING BOX FILE CREATION ***')
    try:
        os.mkdir(OUT_DIR[:-1])
    except Exception:
        print('(Directory "processed" already created, skipping creation...)')
    
    id_track = process_mixed(create_bounding_box)
    process_single(id_track, create_bounding_box)

    print('*** COMPLETE ***')

if __name__ == '__main__':
    main()