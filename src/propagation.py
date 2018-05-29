# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:58:14 2018

@author: malopez
"""
import numpy as np

class Propagator():
    def __init__(self, size_X, size_Y, periodicWalls, periodicSideWalls):
        self.size_X = size_X
        self.size_Y = size_Y
        self.periodicSideWalls = periodicSideWalls
        self.periodicWalls = periodicWalls
    
    
    def propagate(self, t, pos, vel):
        """ Updates positions for all particles, lineal movement during 
            a time t (time until next collision)"""
            
        if str(t)=='inf':
            print('---------------Warning! (inf value is first element)---------------')
        else:
            # Simple propagation of particles
            pos = pos + vel*t
            
            if self.periodicSideWalls==True:
                # If lateral boundary conditions are periodic we need to
                # calculate where the particle needs to appear after leaving
                # the box (only coordinate x in this case)
                pos[:,0] = pos[:,0] - np.floor(pos[:,0]/self.size_X)*self.size_X
                # This is to see how many times it has crossed the box:
                # np.floor(pos[:,0]/self.size_X)*self.size_X
                # Then this is to account for particles leaving both walls:
                # -np.sign(vel[:,0])               
                
            if self.periodicWalls==True:
                # If boundary conditions are periodic we need to
                # calculate where the particle needs to appear after leaving
                # the box
                pos[:,0] = pos[:,0] - np.floor(pos[:,0]/self.size_X)*self.size_X
                pos[:,1] = pos[:,1] - np.floor(pos[:,1]/self.size_Y)*self.size_Y
    
        return pos
