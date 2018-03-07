# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 10:36:56 2018

@author: malopez
"""
from propagation import propagate, advanceTime
from collision import particleCollision, wallCollision
from timeLists import updateCollisionLists

def computeNextCollision(n_particles, particle_radius, size_X, size_Y, 
                         restitution_coef, pos, vel, times_pp, times_pw):
    """ Propagates particles until next collision and updates velocities 
        after it. Checks if next col. is particle-particle or particle-wall """
    #We take the first element (shortest time) of both lists
    t_pp = float(times_pp[0,2])
    t_pw = float(times_pw[0,2])
    # Check if particle-particle or particle-wall collision (or both).
    # I will only comment the first if-clause since the procediment is
    # similar in all cases
    
    # Particle-particle collision case
    if t_pp <= t_pw:
        # Propagates particles until current collision
        pos = propagate(t_pp, n_particles, pos, vel)
        # Advances time
        result = advanceTime(t_pp, times_pp, times_pw)
        times_pp = result[0]
        times_pw = result[1]
        
        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        # Compute change in velocities due to collision
        vel = particleCollision(i, j, vel, pos, particle_radius)
        # And finally, updates the collision time lists with new entries
        result = updateCollisionLists(t_pp, n_particles, particle_radius, 
                                        size_X, size_Y, pos, vel, times_pp, 
                                        times_pw, i, j)
        times_pp = result[0]
        times_pw = result[1]
    
    # Particle-wall collision case
    else:
        pos = propagate(t_pw, n_particles, pos, vel)
        result = advanceTime(t_pw, times_pp, times_pw)
        times_pp = result[0]
        times_pw = result[1]
        
        i = int(times_pw[0,0])
        wall = str(times_pw[0,1])
        vel = wallCollision(i, wall, vel, restitution_coef)
        result = updateCollisionLists(t_pw, n_particles, particle_radius, 
                                      size_X, size_Y, pos, vel, times_pp, 
                                      times_pw, i, j='none')
        times_pp = result[0]
        times_pw = result[1]

    # We return a tuple with the arrays that have changed in this collision
    return (pos, vel, times_pp, times_pw)