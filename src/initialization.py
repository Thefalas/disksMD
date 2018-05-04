# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:49:46 2018

@author: malopez
"""
import numpy as np
from measure import distanceModulus

class RandomGenerator():

    def __init__(self, particle_radius, n_particles, size_X, size_Y):
        
        self.particle_radius = particle_radius
        self.n_particles = n_particles
        self.size_X = size_X
        self.size_Y = size_Y

    def initRandomPos(self):
        """ Initializes particle positions and velocities, makes sure that
            no particles overlap """
    
        # Initialize particle positions as a 2D numpy array.
        pos = np.zeros((self.n_particles, 2), dtype=np.float64)
        
        # Reduced sizes so that particles are not generated inside walls
        reduc_size_X = self.size_X - self.particle_radius
        reduc_size_Y = self.size_Y - self.particle_radius
        
        # First particle is generated in a random position.
        pos[0,0] = np.random.uniform(0+self.particle_radius, reduc_size_X)
        pos[0,1] = np.random.uniform(0+self.particle_radius, reduc_size_Y)
        
        # From 2nd particle on, we need to check if it overlaps previous ones.
        for i in range(1, self.n_particles):
           overlap = False
           # While distance is greater than 2 radius, generates new particles.
           while overlap==False:
               pos[i,0] = np.random.uniform(0+self.particle_radius, reduc_size_X)
               pos[i,1] = np.random.uniform(0+self.particle_radius, reduc_size_Y)
               # Checking that it doesn't overlap with existent particles.
               for j in range(0, i):
                   dist = distanceModulus(i, j, pos[:,0], pos[:,1])
                   overlap = (dist > 2*self.particle_radius)
                   if overlap==False:
                      break

        return pos
    
    def initRandomVel(self):
        """ Initializes particle positions and velocities, makes sure that
            no particles overlap """  
        
        # Initialize particle velocities as a 2D numpy array (normal/gaussian).
        vel = np.random.normal(0, 3, (self.n_particles, 2))

        return vel