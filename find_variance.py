# -*- coding: utf-8 -*-
"""
Created on Sat May  7 18:07:49 2016

@author: efron
"""
import numpy as np

def find_variance(A):
    # find the variance of A
    mean = np.mean(A)
    variance = sum( (a-mean)**2 for a in A) / A.size
    return variance