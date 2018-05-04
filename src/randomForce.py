# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:18:36 2018

@author: malopez
"""
import numpy as np

def randomKick(n_particles, vel, kickIntensity):
    for i in range(n_particles):
        vel[i, 0] = vel[i, 0] * np.random.normal(0, kickIntensity)
        vel[i, 1] = vel[i, 1] * np.random.normal(0, kickIntensity)
    return vel