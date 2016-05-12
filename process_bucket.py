# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:20:55 2016

@author: efron
"""

import numpy as np
from scipy.stats.distributions import chi2  

TINY_NUMBER = 10.**-12

def process_bucket(bucket, init):
    
    """
    subfunctions
    """
    def overlap(bucket, init):
    # if buckets overlap, they should be more similar than chance
    
        row = [block.row for block in bucket]
        col = [block.col for block in bucket]       
        rowDistance = np.abs(row - np.reshape(row, (-1, 1)))
        colDistance = np.abs(col - np.reshape(col, (-1, 1)))
        
        # broadcast to an N x N array    
        rowOverlap = rowDistance < init.blockSize
        colOverlap = colDistance < init.blockSize
        return np.logical_or(rowOverlap, colOverlap)
        
    # calculate test statistic of block-to-block similarity
    def calculate_test_statistic(bucket):
        test_statistic = np.zeros((len(bucket), len(bucket)))    
        for index, subBlock in enumerate(subBlocks):
            pixel_diff = np.sum((subBlock - subBlocks)**2, axis=(1, 2))
            sigmaSq = (variance[index] + variance) / 2.
            # avoid zero divides    
            sigmaSq[sigmaSq < TINY_NUMBER] = (TINY_NUMBER)
            # calcualte test statistic
            test_statistic[index] = pixel_diff / (sigmaSq*subSize)
        return test_statistic
        
    
    # calculate whether blocks are too similar to have occured by chance
    def find_connection(bucket, test_statistic):  
        test_statistic = calculate_test_statistic(bucket)
        MAGIC_THRESHOLD_ADJUSTMENT = 1/(128*2.5)
        # this is a calibration of the pValThreshold to get it to work
        # and is probably not close to ideal. 
        # I need to go back and do the actual math /stats
        # to pick this value more intelligently, but for now it's OK.
        # 5/12/2016
        
        pValThreshold = chi2.ppf(.01, (subSize**2)*MAGIC_THRESHOLD_ADJUSTMENT)
        too_similar = test_statistic < pValThreshold
        
        # blocks are "connected" if they occur by chance < 1% of the time and
        # do not overlap.
        connection = np.ones_like(too_similar)
        connection = np.logical_xor(connection,
        np.logical_or(overlap(bucket, init), np.logical_not(too_similar)))
        return connection
    
    """
    process_bucket body
    """
    
    if len(bucket) == 0:
        # bucket empty, no need to process
        return
    
    subSize = 1
    count = 0
    for block in bucket:
        count += 1
        
    variance = [block.variance for block in bucket]
    count = 0
    while subSize < init.blockSize:
        # sanity check for while loop  
        count +=1
        if count > 10:
            raise(ValueError('process_bucket in infinite loop'))
        
        # expanding block: we start with a 2x2 subblock of the image,
        # test for similarity to other 2x2 subblocks,
        # then continue
        subSize = min(subSize << 1, init.blockSize)
        subBlocks = [1.*block.pixel[0:subSize, 0:subSize] for block in bucket]
        test_statistic = calculate_test_statistic(bucket)
        connection = find_connection(bucket, test_statistic)
        connection = np.any(connection, axis=0)
                
        
        # otherwise, we remove isolated blocks from bucket and let the loop run
        newBucket = []
        for index, block in enumerate(bucket):
            if connection[index]:
                newBucket.append(block)
        if len(newBucket)*init.blockSize < init.minArea:
            return []
        else:
            return newBucket
