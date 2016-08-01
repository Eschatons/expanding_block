# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:20:55 2016

@author: efron
"""

import numpy as np
from scipy.stats.distributions import chi2  

def process_bucket(bucket, init):

    """
    subfunctions
    """

    def find_overlap():
    # if buckets overlap, they should be more similar than chance
        row = [block.row for block in bucket]
        col = [block.col for block in bucket]       

        # broadcast to an N x N array    
        rowDistance = np.abs(row - np.reshape(row, (-1, 1)))
        colDistance = np.abs(col - np.reshape(col, (-1, 1)))
        
        rowOverlap = rowDistance < init.blockSize
        colOverlap = colDistance < init.blockSize

        return np.logical_or(rowOverlap, colOverlap)
        
    # calculate test statistic of block-to-block similarity
    def calculate_test_statistic(subBlocks):
        test_statistic = np.zeros((len(subBlocks), len(subBlocks)))
        variance = [np.var(block) for block in subBlocks]
        
        for index, subBlock in enumerate(subBlocks):
            pixel_diff = np.sum((subBlock - subBlocks)**2, axis=(1, 2))
            sigmaSq = (variance[index] + variance) / 2.

            # avoid zero divides in case of zero-variance blocks
            TINY_NUMBER = 10.**-12
            sigmaSq[sigmaSq < TINY_NUMBER] = (TINY_NUMBER)
            
            test_statistic[index] = pixel_diff / (sigmaSq*subSize)
        return test_statistic
    
        


# calculate whether blocks are too similar to have occured by chance
    def find_connection(test_statistic, overlap):  
        test_statistic = calculate_test_statistic(bucket)        
        pValThreshold = chi2.ppf(.01, (subSize**2))
        too_similar = test_statistic < pValThreshold
        
        # blocks are "connected" if they occur by chance < 1% of the time and
        # do not overlap.
        connection = np.ones_like(too_similar)
        connection = np.logical_xor(connection,
        np.logical_or(overlap, np.logical_not(too_similar)))
        return connection
    
    """
    process_bucket body
    """
    
    if len(bucket) == 0:
        # bucket empty, no need to process
        return []
    
     
    subSize = 1
    overlap = find_overlap()
    while subSize < init.blockSize:
        # expanding block: we start with a 2x2 subblock of the image,
        # test for similarity to other 2x2 subblocks,
        # then continue
        subSize = min(subSize << 1, init.blockSize)
        subBlocks = [1.*block.pixel[0:subSize, 0:subSize] for block in bucket]
        test_statistic = calculate_test_statistic(subBlocks)
        connection = find_connection(test_statistic, overlap)
        connection = np.any(connection, axis=0)
                
        
        # otherwise, we remove isolated blocks from bucket and let the loop run
        bucket = [bucket[n] for n in range(len(bucket)) if connection[n]]
        
        # early exit if area of remaining blocks too small
        if len(bucket)*init.blockSize < init.minArea:
            return []
    # return surviving (i.e, possibly fradulent blocks)
    return bucket