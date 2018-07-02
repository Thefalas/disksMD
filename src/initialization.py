# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:49:46 2018

@author: malopez
"""
import numpy as np

class RandomGenerator():

    def __init__(self, particle_radius, n_particles, size_X, size_Y, baseStateVelocity):
        
        self.particle_radius = particle_radius
        self.n_particles = n_particles
        self.size_X = size_X
        self.size_Y = size_Y
        self.baseStateVelocity = baseStateVelocity

    def initRandomPos(self):
        """ Initializes particle positions and velocities, makes sure that
            no particles overlap """
    
        # Reduced sizes so that particles are not generated inside walls
        reduc_size_X = self.size_X - self.particle_radius
        reduc_size_Y = self.size_Y - self.particle_radius
        
                  
        # Initialize particle positions as a 2D numpy array.
        pos = np.zeros((self.n_particles, 2), dtype=np.float64)
        for i in range(self.n_particles):
            overlap = True
            while overlap == True:
                # While distance is greater than 2 radius, generates new particles.
                pos[i,0] = np.random.uniform(0+self.particle_radius, reduc_size_X)
                pos[i,1] = np.random.uniform(0+self.particle_radius, reduc_size_Y)
                
                # Checking that it doesn't overlap with existent particles.
                distances = self.distanceToCenter(pos[0:i, 0], pos[0:i, 1], pos[i,0], pos[i,1])
                ovlap_particles = np.where(distances <= 2*self.particle_radius)[0]
                # If it overlaps, ignore this iteration and start again the for loop
                # with the same i.
                if len(ovlap_particles)>0:
                    overlap = True
                else:
                    overlap = False

        return pos
    
    def initRandomVel(self):
        """ Initializes particle positions and velocities, makes sure that
            no particles overlap """  
        
        # Initialize particle velocities as a 2D numpy array (normal/gaussian).
        vel = np.random.normal(0, self.baseStateVelocity, (self.n_particles, 2))

        return vel
    
    def distanceToCenter(self, x, y, x_center, y_center):
        """ Simple function, given a pair of coordinates x,y. It returns its
            distances to a central point """
        return np.sqrt((x-x_center)**2 + (y-y_center)**2)
    
    
    def checkNotOverlap(self, pos):
        for i in range(1, self.n_particles):
            distances = self.distanceToCenter(pos[:,0], pos[:,1], pos[i,0], pos[i,1])
            ovlap = np.where(distances <= 2*self.particle_radius)[0]
            if len(ovlap) > 1:
                print(len(ovlap))