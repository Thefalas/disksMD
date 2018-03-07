# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 18:46:23 2018

@author: malopez
"""
import math
import bisect
import numpy as np
from colTimes import detectWallCollisionTime, detectCollisionTime

def createWallCollisionList(n_particles, particle_radius, size_X, size_Y, 
                            pos, vel):
    """ Creates an ordered list times_pw with collision times 
        for all particle-wall events """
    # Initialize two arrays for storing particle-particle and particle-wall
    # collision times; apart from time t, they save the indexes of interacting
    # particles and/or the name of interacting wall.
    part_i = np.array([0 for i in range(n_particles)])
    dt = np.array([0.0 for i in range(n_particles)])
    wall = np.array(['test' for i in range(n_particles)])
    times_pw = np.stack((part_i, wall, dt), axis=1)

    for a in range(n_particles):
        times_pw[a] = detectWallCollisionTime(a, pos, vel, particle_radius, 
                                              size_X, size_Y)
    # Sorting the array for the initialization of the list
    times_pw = times_pw[np.array([float(a) for a in times_pw[:,2]]).argsort()]
    return times_pw

def createCollisionList(n_particles, particle_radius, pos, vel):
    """ Creates an ordered list times_pw with collision times 
        for all particle-particle events """
    # The number of elements in particle-particle collision list is
    # factorial(n)/(2*factorial(n-2)) where n=n_particles
    # This is without repetition (we don't save (3,7) and (7,3); or (5,5) i.e).
    # http://mathworld.wolfram.com/Permutation.html
    n = int(math.factorial(n_particles)/(2*math.factorial(n_particles-2)))
    part_i = np.array([0 for i in range(n)])
    part_j = np.array([0 for i in range(n)])
    dt = np.array([0.0 for i in range(n)])
    times_pp = np.stack((part_i, part_j, dt), axis=1)

    a = 0
    for i in range(n_particles):
        for j in range(i, (n_particles-1)):
            times_pp[a] = detectCollisionTime(i, j+1, pos, vel, particle_radius)
            a = a+1
    # TODO: When ordering i, j are presented in scientific notation ¿why?       
    times_pp = times_pp[times_pp[:,2].argsort()]
    return times_pp
    #times_pp[:,0] = np.array([str(int(a)) for a in times_pp[:,0]])
    #times_pp[:,1] = np.array([str(int(a)) for a in times_pp[:,1]])

def deleteEntries(times_pp, times_pw, i, j='none'):
    """ Delete certain entries containing particles i, j """
    # Solution inspired by: 
    # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-91.php
    if j=='none':
        times_pp = times_pp[~np.isin(times_pp, [float(i)]).any(axis=1)]
        times_pw = times_pw[~np.isin(times_pw, [str(i)]).any(axis=1)]
    else:   
        times_pp = times_pp[~np.isin(times_pp, [float(i), float(j)]).any(axis=1)]
        times_pw = times_pw[~np.isin(times_pw, [str(i), str(j)]).any(axis=1)]
    return (times_pp, times_pw)
            
def updateCollisionLists(t, n_particles, particle_radius, size_X, size_Y, pos, 
                         vel, times_pp, times_pw, i, j='none'):
    """ Deletes and recalculates all entries involving particles that 
        interacted in last collision """
    i = int(i)
    
    if j=='none':
        result = wallCollisionUpdate(t, n_particles, particle_radius, size_X, 
                                     size_Y, pos, vel, times_pp, times_pw, i)
        times_pp = result[0]
        times_pw = result[1]
    else:
        result = partCollisionUpdate(t, n_particles, particle_radius, size_X, 
                                     size_Y, pos, vel, times_pp, times_pw, i, j)
        times_pp = result[0]
        times_pw = result[1]
    
    # We return the updated lists as a tuple
    return (times_pp, times_pw)


def wallCollisionUpdate(t, n_particles, particle_radius, size_X, size_Y, 
                        pos, vel, times_pp, times_pw, i):
    # Particle-Wall collision, recalculates only entries involving part. i
    result = deleteEntries(times_pp, times_pw, i)
    times_pp = result[0]
    times_pw = result[1]
    
    # Particle list update
    # Now we calculate new elements and insert them in an ordered manner
    for a in range(n_particles):
        # Avoid i-i case  and a!=(n_particles-1)
        if (a==i and a!=(n_particles-1)):
            a=a+1
        new_entry = detectCollisionTime(i, a, pos, vel, particle_radius)
        if new_entry[0,2] =='inf':
            index = -1
        else:
            index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
        times_pp = np.insert(times_pp, index, new_entry, axis=0)
       
    # Wall list update
    # Need float conversion due to formating issues with times_pw
    times_pw_float = np.array([float(a) for a in times_pw[:,2]]) 
    new_entry = detectWallCollisionTime(i, pos, vel, particle_radius, 
                                        size_X, size_Y)
    # Bisect is used to compute the index in wich the element would enter
    # a certain list so that it remains ordered
    index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
    times_pw = np.insert(times_pw, index, new_entry, axis=0)
    
    return (times_pp, times_pw)

def partCollisionUpdate(t, n_particles, particle_radius, size_X, size_Y, 
                        pos, vel, times_pp, times_pw, i, j):
    j = int(j)
    # Particle-particle collision, recalculates entries involving i and j.
    result = deleteEntries(times_pp, times_pw, i, j)
    times_pp = result[0]
    times_pw = result[1]
    
    # Particle list update    
    for a in range(n_particles):
        if (a==i and a!=(n_particles-1)): # Avoid i-i case
            a=a+1
        new_entry = detectCollisionTime(i, a, pos, vel, particle_radius)
        if new_entry[0,2] =='inf':
            index = -1
        else:
            index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
        times_pp = np.insert(times_pp, index, new_entry, axis=0)
    for a in range(n_particles):
        # Avoid j-j case and j-i case (already calculated)
        if ((a==j or a==i) and a!=n_particles-1): 
            a=a+1
        new_entry = detectCollisionTime(a, j, pos, vel, particle_radius)
        if new_entry[0,2] =='inf':
            index = -1
        else:
            index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
        times_pp = np.insert(times_pp, index, new_entry, axis=0)
             
    # Wall list update
    new_entry = detectWallCollisionTime(i, pos, vel, particle_radius, 
                                        size_X, size_Y)
    new_entry_j = detectWallCollisionTime(j, pos, vel, particle_radius, 
                                          size_X, size_Y)
    
    times_pw_float = np.array([float(a) for a in times_pw[:,2]])  
    index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
    times_pw = np.insert(times_pw, index, new_entry, axis=0)
    
    times_pw_float = np.array([float(a) for a in times_pw[:,2]])  
    index_j = bisect.bisect(times_pw_float, float(new_entry_j[0,2]))
    times_pw = np.insert(times_pw, index_j, new_entry_j, axis=0)
    
    return (times_pp, times_pw)