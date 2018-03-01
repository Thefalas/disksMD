# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:58:14 2018

@author: malopez
"""
import numpy as np

#eps = 5000*np.finfo(float).eps # Machine epsilon
#eps = 0.0001

def propagate(t, n_particles, pos, vel):
    """ Updates positions for all particles, lineal movement during a time t.
        Modifies the lists containig collision times to reflect the time that
        has passed since last collision """

    for i in range(n_particles):
        pos[i] = pos[i] + vel[i]*t
    return pos
            
def advanceTime(t, times_pp, times_pw):
    # Advances all entries a time t (time since last collision)
    times_pp[:,2] = times_pp[:,2] - t
    times_pw[:,2] = np.array([float(a) for a in times_pw[:,2]]) - t
    
    return (times_pp, times_pw)