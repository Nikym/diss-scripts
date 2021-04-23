import cv2
import os
import json
from shared_resources import ROOT_DIR, OUT_DIR, NUM_SETS, process_mixed, process_single

def convert_images(scene_path: str, scene_id: str, out_path: str, new_id: str):
    '''
    Convert images to the required names and formats.

        Parameters:
            scene_path (str): Path to the original scene directory
            scene_id (str): ID of the scene
            out_path (str): Path to the output directory
            new_id (str): New synchronised ID of scene
    '''
    color_img = cv2.imread(scene_path + scene_id + '.png')
    cv2.imwrite(out_path + new_id + '-color.png', color_img)

    depth_img = cv2.imread(scene_path + scene_id + '.depth.16.png', -1)
    cv2.imwrite(out_path + new_id + '-depth.png', depth_img)

    seg_img = cv2.imread(scene_path + scene_id + '.cs.png', cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(out_path + new_id + '-label.png', seg_img)

def main():
    print('*** BEGINNING PROCESSING OF IMAGES ***')
    try:
        os.mkdir(OUT_DIR[:-1])
    except Exception:
        print('(Directory "processed" already created, skipping creation...)')
    
    id_track = process_mixed(convert_images)
    process_single(id_track, convert_images)

    print('*** COMPLETE ***')

if __name__ == '__main__':
    main()