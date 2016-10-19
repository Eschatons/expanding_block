# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:34:13 2016

@author: efron
"""

""" create_mask"""

import numpy as np
from block_class import ExpandingBlockInit
from skimage import color


RED, GREEN, BLUE = 0, 1, 2


FLAG_FILL    = 0b0100
FLAG_REMOVE  = 0b1000

def create_mask(blocks:list, img:np.ndarray, 
                init:ExpandingBlockInit) -> np.ndarray:
    ''' create mask: this is a 2d boolean matrix of the same dimensions as the 
     original image, set to True in blocks that are connected to other blocks
    (i.e, considered possibly copy-paste forged) and false elsewhere '''
    rows = np.shape(img)[0]
    cols = np.shape(img)[1]
    mask = np.zeros((rows, cols, 3), 'uint8')
    
    for block in blocks:
        row = block.row
        col = block.col
        rowEnd = row + init.blockSize
        colEnd = col + init.blockSize
        
        mask[row:rowEnd, col:colEnd, RED] = FLAG_FILL
        mask[row:rowEnd, col:colEnd, BLUE] = FLAG_REMOVE
        mask[row:rowEnd, col:colEnd, GREEN] = FLAG_REMOVE
    return mask
    
def write_mask(mask: np.ndarray, img: np.ndarray) -> np.ndarray:
    ''' we create an image image_out which is the original image on the left, a
     8-row BLUE (0, 0, 255) barrier, and then a MASKED image on the right.
     The MASKED image is a grayscale version of the original image, except that
    and set to RED (255, 0, 0) where the MASK is True 
     (i.e, blocks considered modified) '''
    
    # create psuedo-rgb grayscale version of image
    imgMasked = np.uint8(255*color.gray2rgb(color.rgb2gray(img)))
    # cover with mask to mark forged areas
    imgMasked[mask==FLAG_FILL] = 255
    imgMasked[mask==FLAG_REMOVE] = 0
    rows = np.shape(img)[0]
    separator = np.ones((rows, 16, 3), 'uint8')*255
    imgOut = np.concatenate((img, separator, imgMasked), axis=1)
    return imgOut