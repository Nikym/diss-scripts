# FAT to YCB Data Processing Scripts

The following set of scripts allow for easy conversion from the Falling Things dataset file / image structure to that of the YCB dataset. Similarly, this also works for the outputs of the NDDS plugin for UE4.

Used for data prep for training PoseCNN.

## The Scripts
* `common_funcs.py` - Contains shared functions and variables such as the `ROOT_PATH`.
* `img_conv.py` - Downsizes images to the size required by PoseCNN as well converting from JPEG to PNG.
* `bounding_box.py` - Creates files containing bounding box data for each object in a scene (per file).
* `fat_to_ycb_meta.py` - Creates `.mat` files in the same format as YCB dataset. Excludes creating of `vertmap` attribute.
* `img_seg_adjust.py` - Modifies pixel values in `*-label.png` images to ensure segmentation IDs remain consistent for each object.
* `generate_train_file.py` - Generates the `train.txt` file for use by PoseCNN. Quite specific directory structure required.