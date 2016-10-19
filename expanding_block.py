# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:53:35 2016

@author: efron
"""

"""
expanding_block
"""

import numpy as np
from block_class import Block, ExpandingBlockInit
from skimage import io, color
from mask import create_mask, write_mask
from process_bucket import process_bucket
from itertools import dropwhile

        
def expanding_block(filename, *, _debug = False):
    """
Tests an image for copy-move forgery (a portion of an image has been copied
and then moved somewhere else within the image.)

Written by Efron Licht, based off the algorithm
"An efficient expanding block algorithm for image copy-move forgery detection"
by Gavin Lynch, Frank Y. Shih, and Hong-Yuan Mark Liao, and published in
Information Sciences 239 in 2013.

Free for noncommerical use or modification, but please retain the above credits.
Please ask for commerical use.

input:
    filename that contains an mxn image (color or grayscale)
    known valid formats: '.png', '.jpg'

output:
    imageConsideredModified, imgOut
    where imageConsideredModified is True | False
    if imageConsideredModified == True,     imgOut is the original image
    if imageConsideredModified == False,    imgOut is a (2m+8) x n x 3 image
    """

    """ 
    helper functions
    """

    def _generate_groups(blocks):
        """ assign blocks within image evenly to groups"""
        group = []
        blocksPerGroup = len(blocks) / init.numBuckets
        group = 0
        count = 0

        for block in blocks:
            if len(group) >= blocksPerGroup:
                yield group
                count -= blocksPerGroup
                group = []
            group.append(block)
            count += 1
        if len(group) > 0:
            yield group
            
    def _generate_buckets(groups):
        """ assign blocks within groups to overlapping buckets """
        for n in range(len(groups)):
            try:
                bucket = groups[n-1] + groups[n] + groups[n+1]
            except IndexError:
                if n == init.numBuckets-1:
                    bucket = groups[n-1]+groups[n]
                else:
                    raise
            yield bucket
    
    """
    MAIN FUNCTION START
    """
    #0. file IO and conversion to grayscale:

    baseImg = io.imread(filename)

    try:
        # color.rgb2gray converts to doubles on unit scale (0<pixel<1)
        # so we rescale back to uint8

        img = np.uint8(255*color.rgb2gray(baseImg))

    except ValueError:
        shape = np.shape(baseImg)
        if shape[2] == 1:   # image is grayscale already
            img = baseImg
            # convert image into a a 3D array (psuedo-RGB) so as to not handle
            # so many unique cases later
            baseImg = np.uint8(255*color.gray2rgb(baseImg))
        else:
            raise

    init = ExpandingBlockInit(img)

    rows, cols, *_ = np.shape(img)-init.blockSize
    blocks = ((Block(img, row, col, init) 
        for row in range(rows) 
        for col in range(cols))
        )
    blocks = sorted(blocks, key = lambda block: block.variance)

    #1. remove elements with too low of variance to cut down on false positives
    #    due to bad white balance on source camera or areas of block color
    
    blocks = dropwhile(lambda block: block.tooLowVariance, blocks)
    
    #2. assign blocks as evenly as possible to groups
    groups = _generate_groups(blocks)
    
    #3. assign blocks in neighboring groups to overlapping buckets
    buckets = _generate_buckets(groups)
    
    #4. process buckets for pixel-to-pixel similiarity. see process_bucket
    buckets = (process_bucket(bucket) for bucket in buckets)
    
    
    #buckets now hold blocks that we think are modified.
    #5. recombine buckets after processing
    blocks = [block for bucket in buckets for block in bucket]
    #6a. Image is considered clean if no blocks left after processing
    if len(blocks) == 0:


        imageConsideredModified = False
        imgOut = baseImg    
    #6b. If image is considered modified,create mask for image
    else:
        imageConsideredModified = True

        mask = create_mask(blocks, baseImg, init)
    #7b. Paint mask over image
        imgOut = np.uint8(write_mask(mask, baseImg))
    #8. Output.
    if _debug:
        io.imshow(imgOut)
    
    return imageConsideredModified, imgOut
