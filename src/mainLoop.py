# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 10:36:56 2018

@author: malopez
"""
from propagation import propagate, advanceTime #frictionVelocityChange
from collision import particleCollision, wallCollision
from timeLists import updateCollisionLists

def computeNextCollision(n_particles, particle_radius, mu, size_X, size_Y, 
                         restitution_coef, pos, vel, times_pp, times_pw, 
                         abs_time):
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
        pos = propagate(t_pp, mu, pos, vel)
        """vel = frictionVelocityChange(t_pp, n_particles, mu, vel)"""
        # Advances time
        times_pp, times_pw = advanceTime(t_pp, times_pp, times_pw)

        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        # Compute change in velocities due to collision
        vel = particleCollision(i, j, vel, pos, particle_radius)
        # And finally, updates the collision time lists with new entries
        times_pp, times_pw = updateCollisionLists(t_pp, n_particles, 
                                                  particle_radius, size_X, 
                                                  size_Y, pos, vel, times_pp, 
                                                  times_pw, i, j)
        
        abs_time += t_pp # We update the value for absolute time
    
    # Particle-wall collision case
    else:
        pos = propagate(t_pw, mu, pos, vel)
        """vel = frictionVelocityChange(t_pw, n_particles, mu, vel)"""
        
        times_pp, times_pw = advanceTime(t_pw, times_pp, times_pw)
        
        i = int(times_pw[0,0])
        wall = str(times_pw[0,1])
        vel = wallCollision(i, wall, vel, restitution_coef)
        times_pp, times_pw = updateCollisionLists(t_pw, n_particles, particle_radius, 
                                      size_X, size_Y, pos, vel, times_pp, 
                                      times_pw, i, j='none')
        
        abs_time += t_pp

    # We return a tuple with the arrays that have changed in this collision
    return pos, vel, times_pp, times_pw, abs_time