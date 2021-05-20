# -*- coding: utf-8 -*-
"""
Created on Wed May 19 13:04:47 2021

@author: Ricky
"""

import os
from os.path import join as oj
import cv2
from tqdm import tqdm       # For progress bar

# variables to hold the relevant directory paths.
parent_masks_dir = oj('..', 'data', 'masks')
raw_mask_dir     = oj(parent_masks_dir, 'segmentation-binary')
dil_path         = oj(parent_masks_dir, 'dilated-masks')             # Directory to hold original mask with dilation applied.
diff_path        = oj(parent_masks_dir, 'dilated-masks-diff')         # To hold the difference between the original & the dilated masks.
dil_path_256     = oj(parent_masks_dir, 'dilated-masks-256')         # To hold raw resized masks (256x256).
diff_path_256    = oj(parent_masks_dir, 'dilated-masks-diff-256')    # To hold dilated masks after resizing.

# create the relevant directories if they don't exist.
os.makedirs(dil_path, exist_ok=True)
os.makedirs(diff_path, exist_ok=True)
os.makedirs(dil_path_256, exist_ok=True)
os.makedirs(diff_path_256, exist_ok=True)


def dilate_ims(dil_path, diff_path, new_size = None):
    """ new_size should be a tuple (width, height)"""
    
    for file in tqdm(os.listdir(raw_mask_dir)):
        file_path = oj(raw_mask_dir, file)      # Path to the raw mask.
    
        img = cv2.imread(file_path, 0)                               # Read the binary mask in grayscale.
        
        if new_size is not None:                                     # If sizing parameter supplied then first resize the image.
            img = cv2.resize(img, new_size)
        
        strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))  # Create a rounded structuring element for dilation.
        
        img_dil = cv2.dilate(img,strel,iterations = 1)               # Apply dilation to the mask.
        
        img_diff = img_dil - img                                     # Get the pixels we have added to the mask.
        
        try:                                                         # Write both the dilated image & diff to file.
            cv2.imwrite(oj(dil_path, file), img_dil)
            cv2.imwrite(oj(diff_path, file), img_diff)  
        except:                                                      # If an error occurs, print filename to screen.
            print(file) 


# Run dilation for the original images and also resize.
dilate_ims(dil_path, diff_path)                                       
dilate_ims(dil_path_256, diff_path_256, (256, 256))    