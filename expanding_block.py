# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:53:35 2016

@author: efron
"""

"""
expanding_block
"""

import numpy as np
import os, sys, direct
cwd = os.getcwd()
from block_class import Block, ExpandingBlockInit
from skimage import io, color
from process_bucket import process_bucket
from mask import create_mask, write_mask
def IMPORT_PLACEHOLDER():
    pass

filename = 'garbage'

"""
file IO and conversion to grayscale:
"""
baseImg = io.imread(filename)
try:
    img = color.rgb2gray(baseImg)
except ValueError as valError:
    shape = np.shape(baseImg)
    if shape[2] == 1:   # image is grayscale already
        img = baseImg
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

    
image = None # pass
size = np.shape(img)
rows = size[0]
cols = size[1]
# list comprehensions make this whole next section way easier!
blocks = [Block(row, col, init) for row in range(rows-init.blockSize) 
    for col in range(cols-init.blockSize)]
# sort by variance    
blocks.sort(key = lambda x: x.variance)

"""
remove elements with too low of variance
causes false positives due to bad white balance on camera or just areas of 
block color
"""
# this is not efficient, but it is negligible in comparison to overhead of 
# other parts of program, and it's a neat bit of set theory.

blocks = [block for block in blocks if not block.tooLowVariance]
groups = []
# assign blocks to groups
blocksPerBucket = len(blocks) / init.numBuckets
group = 0
count = 0
for block in enumerate(blocks):
    count += 1
    groups[group].append = block
    if count > blocksPerBucket:
        count -= blocksPerBucket
        # group is full, move on to next group
        groups.append([])

    
# assign groups to buckets
buckets = [None]*init.numBuckets

for n in range(init.numBuckets):
    buckets[n] = group[n-1] + group[n] + group[n+1]

"""
process buckets for pixel-to-pixel similiarity
"""
buckets = [process_bucket(bucket) for bucket in buckets]

""" recombine buckets after processing, removing empty buckets """
blocks = [bucket for bucket in buckets if len(bucket) > 0]

mask = create_mask(blocks, baseImg)
imgOut = write_mask(blocks, baseImg)