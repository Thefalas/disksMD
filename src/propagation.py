# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:58:14 2018

@author: malopez
"""

def propagate(t, pos, vel):
    """ Updates positions for all particles, lineal movement during 
        a time t (time until next collision)"""
        
    if str(t)=='inf':
        print('---------------Warning! (inf value is first element)---------------')
    else:
        pos = pos + vel*t #- (0.5*as2DArray(mu,vel[i])*t*t) # Including friction

    return pos
