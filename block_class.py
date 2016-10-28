# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:04:19 2016

@author: efron
"""

"""
Class Definitions for expanding_block
"""

import numpy as np





class ExpandingBlockInit:
    """ customizable settings to adjust for image size """
    def __init__(self, img: np.ndarray):
        size = np.shape(img)[0]*np.shape(img)[1]
        
        # varianceThreshold are 'magic numbers' chosen by trial and error to get
        # the damn thing to work with acceptable True Positive / False Negative
        # True Negative / False Positive rates
        # I don't think they're even close to ideal, but for now this is OK.
        # 5/12/2016
        
        if size <= 50**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 400
            self.minArea = 32
            self.varianceThreshold = 2*self.blockSize**2
        elif size <= 100**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 400
            self.minArea = 55
            self.varianceThreshold = 4*self.blockSize**2
        elif size <= 200**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 600
            self.minArea = 55
            self.varianceThreshold = 2*self.blockSize**2
        elif size <= 350**2:
            self.blockSize = 8
            self.blockDistance = 1
            self.numBuckets = 5000
            self.minArea = 55
            self.varianceThreshold = 2*self.blockSize**2
        elif size <= 700**2:
            self.blockSize = 16
            self.blockDistance = 1
            self.numBuckets = 12000
            self.minArea = 100
            self.varianceThreshold = 4*self.blockSize**2
        else: # image larger than 4900000 pixels
            self.blockSize = 16
            self.blockDistance = 1
            self.numBuckets = size // 128
            self.minArea = 120
            self.varianceThreshold = 4*self.blockSize**2
            
class Block:
    """ overlapping blocks of the image that are compared
    to find copy-paste forgery """
    def __init__(self, img:np.ndarray, row:int, col:int, init:ExpandingBlockInit):
        rowEnd = row+(init.blockSize-1)
        colEnd = col+(init.blockSize-1)
        self.pixel = (img[row:rowEnd, col:colEnd])
        # actual pixels of the block
        self.row = row  # start of row
        self.col = col  # start of column
        self.init = init # hold reference to init for __repr__
        self.variance = np.var(self.pixel)
        # variance of pixels: mean((pixel-mean(pixels))**2)
        self.tooLowVariance = self.variance < (init.varianceThreshold)
		self.sourceImg = img
        # boolean: if true, we eliminate the block and don't consider it
    def __str__(self):
        return 'Block: row = {0}, col = {1}, pixel = {2}'.format(self.row, self.col, self.pixel)
        
    def __repr__(self):
		return 'Block{img = {0}, row = {1}, col = {2}, init = {3}'.format(self.sourceImg, self.row, self.col, self.init)
    def __getitem__(self, key):
        return self.pixel[key]
    def __setitem__(self, key, value):
        self.pixel[key] = value
    def __contains__(self, key):
        return key in self.pixel
    def __len__(self):
        return len(self.pixel)
    