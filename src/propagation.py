# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:58:14 2018

@author: malopez
"""
import numpy as np

def propagate(t, pos, vel):
    """ Updates positions for all particles, lineal movement during 
        a time t (time until next collision)"""
        
    if str(t)=='inf':
        print('---------------Warning! (inf value is first element)---------------')
    else:
        pos = pos + vel*t #- (0.5*as2DArray(mu,vel[i])*t*t) # Including friction

    return pos

"""def frictionVelocityChange(t, n_particles, mu, vel):
    vel = vel - as2DArray(mu, vel)*t
    return vel"""
            
def advanceTime(t, times_pp, times_pw):
    """ Advances all entries a time t (time since last collision) """
    times_pp[:,2] = times_pp[:,2] - t
    times_pw[:,2] = np.array([float(a) for a in times_pw[:,2]]) - t
    
    return times_pp, times_pw

def as2DArray(mu, array):
    
    result = np.sign(array)*np.array([mu, mu])
    return result