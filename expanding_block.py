# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:53:35 2016

@author: efron
"""

"""
expanding_block
"""

DEBUG = True

import numpy as np
from block_class import Block, ExpandingBlockInit
from skimage import io, color
from mask import create_mask, write_mask
from process_bucket import process_bucket

def expanding_block(filename):

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
    file IO and conversion to grayscale:
    """
    baseImg = io.imread(filename)

    try:
        # color.rgb2gray converts to doubles on unit scale (0<pixel<1)
        # so we rescale back to uint8

        img = np.uint8(255*color.rgb2gray(baseImg))

    except ValueError as valError:
        shape = np.shape(baseImg)
        if shape[2] == 1:   # image is grayscale already
            img = baseImg
            # convert image into a a 3D array (psuedo-RGB) so as to not handle
            # so many unique cases later
            baseImg = np.uint8(255*color.gray2rgb(baseImg))
        else:
            raise valError
    except Exception as exc:
        raise exc
    """
    set parameters based off image size

    """
    init = ExpandingBlockInit(img)

    """
    Divide the image into small overlapping blocks of blockSize ** 2
    """
    #img = Image.open(filename)

    rows = np.shape(img)[0]-init.blockSize
    cols = np.shape(img)[1]-init.blockSize
    blocks = ([Block(img, row, col, init)
        for row in range(rows) for col in range(cols)])

    def byVariance_key(block):
        return block.variance

    blocks = sorted(blocks, key = byVariance_key)

    """
    remove elements with too low of variance to cut down on false positives
    due to bad white balance on source camera or areas of block color

    """

    blocks = [block for block in blocks if not block.tooLowVariance]

    """
    assign blocks to groups
    """

    groups = [ [] for x in range(init.numBuckets)]
    # we don't want to use * to avoid nasty by-reference bugs
    blocksPerBucket = len(blocks) / init.numBuckets
    group = 0
    count = 0

    for block in blocks:
        try:
            groups[group].append(block)
            count += 1
        except IndexError:
            print('trying to assign to group ' + str(group) + ' when')
            print('init.numBuckets = ' + str(init.numBuckets))
            raise IndexError


        if count >+ blocksPerBucket:
            group += 1
            count -= blocksPerBucket
    """
    assign groups to buckets
    """
    buckets = [None]*init.numBuckets
    for n in range(init.numBuckets):
        try:
            buckets[n] = groups[n-1] + groups[n] + groups[n+1]
        except IndexError:
            if n == init.numBuckets-1:
                buckets[n] = groups[n-1]+groups[n] + groups[-1]
            else:
                raise IndexError
    """
    process buckets for pixel-to-pixel similiarity
    """    
    buckets = [process_bucket(bucket, init) for bucket in buckets]
    """
    recombine buckets after processing, removing empty buckets
    """
    blocks = []
    for bucket in buckets:
        for block in bucket:
            blocks.append(block)

    """
    if there are no blocks left, the image is clean
    """
    if len(blocks) == 0:
        imageConsideredModified = False
        return imageConsideredModified, baseImg
    #else
    imageConsideredModified = True

    """
    otherwise, we create a masked image to show where the
    modification occured
    """
    mask = create_mask(blocks, baseImg, init)
    imgOut = np.uint8(write_mask(mask, baseImg))
#    io.imshow(imgOut)
    return imageConsideredModified, imgOut
