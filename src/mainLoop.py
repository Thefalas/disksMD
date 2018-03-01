# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 10:36:56 2018

@author: malopez
"""
from propagation import propagate, advanceTime
from collision import particleCollision, wallCollision
from timeLists import updateCollisionLists

def computeNextCollision(n_particles, particle_radius, size_X, size_Y, restitution_coef, pos, vel, times_pp, times_pw):
    """ Propagates particles until next collision and updates velocities 
        after it. Checks if next col. is particle-particle or particle-wall """
    t_pp = float(times_pp[0,2])
    t_pw = float(times_pw[0,2])
    # Check if particle-particle or particle-wall collision
    if t_pp <= t_pw: # TODO: Habria que añadir el caso en el que los tiempos fueran igual, calcular las dos colisiones, otro elif ------------
        # Propagate particles until current collision
        pos = propagate(t_pp, n_particles, pos, vel)
        result = advanceTime(t_pp, times_pp, times_pw)
        times_pp = result[0]
        times_pw = result[1]
        
        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        # Compute change in velocities due to collision
        vel = particleCollision(i, j, vel, pos, particle_radius)

        result = updateCollisionLists(t_pp, n_particles, particle_radius, 
                                        size_X, size_Y, pos, vel, times_pp, 
                                        times_pw, i, j)
        times_pp = result[0]
        times_pw = result[1]
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

    return (pos, vel, times_pp, times_pw)