# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:34:13 2016

@author: efron
"""

""" create_mask"""

import numpy as np
def create_mask(blocks, img, init):
    size = np.shape(img)
    rows = size[0]
    cols = size[1]
    mask = np.zeros(rows, cols)
    for block in blocks:
        row = block.row
        col = block.col
        rowEnd = row +init.blockSize-1
        colEnd = col + init.blockSize-1
        mask[row:rowEnd][:, col:colEnd] = True        
    return mask
    
def write_mask(blocks, img, init):
    