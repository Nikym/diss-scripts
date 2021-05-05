# FAT to YCB Data Processing Scripts 

The following set of scripts allow for easy conversion from the "Falling Things" dataset file / image structure to that of the YCB dataset. Similarly, this also works for the outputs of the NDDS plugin for UE4.

Used for data prep for training PoseCNN.

## The Scripts
 - `FAT_v2` directory contains scripts to process the Falling Things dataset. 
 - `ndds` directory contains scripts to process the generated data from the NDDS plugin.

 The `FAT` directory contains an older version of the FAT processing scripts. If executing those, execute in the following order:
 - `img_conv.py`
 - `bounding_box.py`
 - `fat_to_ycb_meta.py`
 - `img_seg_adjust.py`
 - `mat_id_change.py`

 If running the newer versions of the scripts, use the following order:
 - `process_images.py`
 - `process_box.py`
 - `process_mat.py`

 Or, if present, use call the `process.sh` bash script from the root directory of this repository. (eg, `bash ./ndds/process.sh`)
 