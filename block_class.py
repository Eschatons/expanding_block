# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:04:19 2016

@author: efron
"""

"""
Class Definitions for expanding_block
"""

import find_variance
import numpy as np

""" overlapping blocks of the image that are compared to find copy-paste forgery """
class Block:
    def __init__(self, img, row, col, init):
        rowEnd = row+(init.blockSize-1)
        colEnd = col+(init.blockSize-1)
        self.pixel = (img[row:rowEnd][:, col:colEnd])
        # actual pixels of the block
        self.row = row  # start of row
        self.col = col  # start of column
        self.variance = find_variance(self.pixel)
        # variance of pixels: mean((pixel-mean(pixels))**2)
        
        self.tooLowVariance = self.variance < init.varianceThreshold 
        # boolean: if true, we eliminate the block and don't consider it
        

""" customizable settings to adjust for image size """
class ExpandingBlockInit:
    def __init__(self, img):
        shape = np.shape(img)
        size = shape[0]*shape[1]
        
        if size <= 50**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 400
            self.minArea = 32
            self.varianceThreshold = 8*4
        elif size <= 100**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 400
            self.minArea = 50
            self.varianceThreshold = 8*4
        elif size <= 200**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 600
            self.minArea = 50
            self.varianceThreshold = 8*4
        elif size <= 350**2:
            self.blockSize = 16
            self.blockDistance = 1
            self.numBuckets = 5000
            self.minArea = 50
            self.varianceThreshold = 16*4
        elif size <= 700**2:
            self.blockSize = 16
            self.blockDistance = 1
            self.numBuckets = 12000
            self.minArea = 70
            self.varianceThreshold = 16*4
        else:
            self.blockSize = 16
            self.blockDistance = 1
            self.numBuckets = size // 128
            self.minArea = 70
            self.varianceThreshold = 16*4