# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:34:13 2016

@author: efron
"""

""" create_mask"""

import numpy as np
from skimage import color, io

RED = 0
GREEN = 1
BLUE = 2
FILL_CHANNEL = 4
REMOVE_CHANNEL = 8
def create_mask(blocks, img, init):
    # create mask: this is a 2d boolean matrix of the same dimensions as the 
    # original image, set to True in blocks that are connected to other blocks
    # (i.e, considered possibly copy-paste forged) and false elsewhere
    rows = np.shape(img)[0]
    cols = np.shape(img)[1]
    mask = np.zeros((rows, cols, 3), 'uint8')
    for block in blocks:
        row = block.row
        col = block.col
        rowEnd = row + init.blockSize
        colEnd = col + init.blockSize
        mask[row:rowEnd, col:colEnd, RED] = FILL_CHANNEL
        mask[row:rowEnd, col:colEnd, BLUE] = REMOVE_CHANNEL
        mask[row:rowEnd, col:colEnd, GREEN] = REMOVE_CHANNEL
    return mask
    
def write_mask(mask, img):
    # we create an image image_out which is the original image on the left, a
    # 8-row BLUE (0, 0, 255) barrier, and then a MASKED image on the right.
    # The MASKED image is a grayscale version of the original image, except that
    # and set to RED (255, 0, 0) where the MASK is True 
    # (i.e, blocks considered modified)
    
    # create psuedo-rgb grayscale version of image
    
    imgMasked = np.uint8(255*color.gray2rgb(color.rgb2gray(img)))
    imgMasked[mask==FILL_CHANNEL] = 255
    imgMasked[mask==REMOVE_CHANNEL] = 0
    rows = np.shape(img)[0]
    separator = np.zeros((rows, 8, 3), 'uint8')
    separator[:, :, BLUE] = 255
    imgOut = np.concatenate((img, separator, imgMasked), axis=1)
    return imgOut