# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:49:46 2018

@author: malopez
"""
import random
import numpy as np
from measure import distanceModulus

def initRandomPos(particle_radius, n_particles, size_X, size_Y):
    """ Initializes particle positions and velocities, makes sure that
        no particles overlap """
    pos_X = np.array([0.0 for i in range(n_particles)])
    pos_Y = np.array([0.0 for i in range(n_particles)])
    # Initialize particle positions as a 2D numpy array.
    pos = np.stack((pos_X, pos_Y), axis=1)
    
    # Reduced sizes so that particles are not generated inside walls
    reduc_size_X = size_X - particle_radius
    reduc_size_Y = size_Y - particle_radius
    # First particle is generated in a random position.
    pos_X[0] = random.uniform(0+particle_radius, reduc_size_X)
    pos_Y[0] = random.uniform(0+particle_radius, reduc_size_Y)
    # From 2nd particle we need to check if it overlaps with previous ones.
    for i in range(1, n_particles):
       overlap = False
       # While the distance is greater than 2 radius, generates new particles.
       while overlap==False:
           pos_X[i] = random.uniform(0+particle_radius, reduc_size_X)
           pos_Y[i] = random.uniform(0+particle_radius, reduc_size_Y)
           # Checking that it doesn't overlap with existent particles.
           for j in range(0, i):
               dist = distanceModulus(i, j, pos_X, pos_Y)
               overlap = (dist > 2*particle_radius)
               if overlap==False:
                  break
    pos = np.stack((pos_X, pos_Y), axis=1)
    return pos

def initRandomVel(n_particles):
    """ Initializes particle positions and velocities, makes sure that
        no particles overlap """  
    vel_X = np.array([random.uniform(-5, 5) for i in range(n_particles)])
    vel_Y = np.array([random.uniform(-5, 5) for i in range(n_particles)])
    # Initialize particle velocities as a 2D numpy array.
    vel = np.stack((vel_X, vel_Y), axis=1) #Deberia ser una dist gaussiana
    return vel