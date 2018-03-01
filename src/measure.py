# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:54:51 2018

@author: malopez
"""
import math

def distance(i, j, pos):
    """ Returns the distance between two particles i, j as a numpy array """
    i = int(i)
    j = int(j)
    dist = pos[i] - pos[j]
    return dist

def distanceModulus(i, j, pos_X, pos_Y):
    """ Measures the distance modulus between two particles i, j """
    i = int(i)
    j = int(j)
    dist_X = pos_X[j] - pos_X[i]
    dist_Y = pos_Y[j] - pos_Y[i]
    dist = math.sqrt(dist_X*dist_X + dist_Y*dist_Y)
    return dist

def relativeVelocity(i, j, vel):
    """ Measures the relative velocity between two particles i, j """
    i = int(i)
    j = int(j)
    rel_v = vel[i] - vel[j]
    return rel_v