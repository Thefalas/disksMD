# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:02:54 2018

@author: malopez
"""
import numpy as np
from measure import distance, relativeVelocity

def wallCollision(i, wall, vel, restitution_coef):
    i = int(i)
    wall = str(wall)

    if (wall=='left' or wall=='right'):
        vel[i,0] = -restitution_coef * vel[i,0] # x component changes direction
    elif (wall=='top' or wall=='bottom'):
        vel[i,1] = -restitution_coef * vel[i,1] # y component changes direction

def particleCollision(i, j, vel, pos, particle_radius):
    i = int(i)
    j = int(j)
    
    r = distance(i, j, pos)
    v = relativeVelocity(i, j, vel)
    b = np.dot(r, v)
    # The following formula has been taken from Eq: 14.2.4 in
    # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
    delta_v = (-b/(4*particle_radius*particle_radius))*r
    # TODO: a mass parameter would be useful whe expanding functionality
    vel[i] = vel[i] + delta_v 
    vel[j] = vel[j] - delta_v