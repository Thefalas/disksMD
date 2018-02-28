# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:53:33 2018

@author: malopez
"""
import math

def infIfNegative(t):
    if t <= 0:
        return 'inf'
    else:
        return t

def nanIfNegative(t):
    if t <= 0:
        return math.nan
    else:
        return t
