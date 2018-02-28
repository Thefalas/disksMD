"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
import math
import bisect
#import json
from operator import itemgetter, attrgetter
import numpy as np
from initialization import initRandomPos, initRandomVel
from tools import saveData#, loadSettings
from collision import wallCollision, particleCollision
from colTimes import detectCollisionTime, detectWallCollisionTime
from propagation import propagate, advanceTime

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
eps = 5000*np.finfo(float).eps # Machine epsilon

# Loading parameters from settings json file
# loadSettings()

restitution_coef = 1.0
particle_radius = 1.0
n_particles = 30
desired_collisions_per_particle = 50
n_collisions = n_particles*desired_collisions_per_particle

scale_factor = 25
form_factor = 16/9

size_X = scale_factor*particle_radius
size_Y = scale_factor*particle_radius/form_factor

# Initialize two arrays for storing particle-particle and particle-wall
# collision times; apart from time t, they save the indexes of interacting
# particles and/or the name of interacting wall.
part_i = np.array([0 for i in range(n_particles)])
dt = np.array([0.0 for i in range(n_particles)])
wall = np.array(['test' for i in range(n_particles)])

times_pw = np.stack((part_i, wall, dt), axis=1)
# The number of elements in particle-particle collision list is
# factorial(n)/(2*factorial(n-2)) where n=n_particles
# This is without repetition (we don't save (3,7) and (7,3); or (5,5) i.e).
# http://mathworld.wolfram.com/Permutation.html
pp_elements = int(math.factorial(n_particles)/(2*math.factorial(n_particles-2)))
part_i = np.array([0 for i in range(pp_elements)])
part_j = np.array([0 for i in range(pp_elements)])
dt = np.array([0.0 for i in range(pp_elements)])

times_pp = np.stack((part_i, part_j, dt), axis=1)
        
def createWallCollisionList():
    """ Creates an ordered list times_pw with collision times 
        for all particle-wall events """
    global times_pw
    for a in range(n_particles):
        times_pw[a] = detectWallCollisionTime(a, pos, vel, particle_radius, size_X, size_Y)
    times_pw = times_pw[np.array([float(a) for a in times_pw[:,2]]).argsort()]

def createCollisionList():
    """ Creates an ordered list times_pw with collision times 
        for all particle-particle events """
    global times_pp
    a = 0
    for i in range(n_particles):
        for j in range(i, (n_particles-1)):
            times_pp[a] = detectCollisionTime(i, j+1, pos, vel, particle_radius)
            a = a+1
    # TODO: When ordering i, j are presented in scientific notation ¿why?       
    times_pp = times_pp[times_pp[:,2].argsort()] 
    #times_pp[:,0] = np.array([str(int(a)) for a in times_pp[:,0]])
    #times_pp[:,1] = np.array([str(int(a)) for a in times_pp[:,1]])
            
def updateCollisionLists(t, i, j='none'):
    """ Deletes and recalculates all entries involving particles that 
        interacted in last collision """
    global times_pp, times_pw
    i = int(i)
    
    if j=='none':
        # Particle-Wall collision, recalculates only entries involving part. i
        # Delete certain entries, solution inspired by:
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-91.php
        times_pp = times_pp[~np.isin(times_pp, [i]).any(axis=1)] ################################ por aqui quiza esta el problema, refactorizar para usar listas
        times_pw = times_pw[~np.isin(times_pw, [str(i)]).any(axis=1)]
    
        # Need float conversion due to formating issues with times_pw
        times_pw_float = np.array([float(a) for a in times_pw[:,2]])
        # Now we calculate new elements and insert them in an ordered manner
        for a in range(n_particles):
            if (a==i and a!=(n_particles-1)): # Avoid i-i case
                a=a+1
            new_entry = detectCollisionTime(i, a, pos, vel, particle_radius)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        
        # Wall update
        new_entry = detectWallCollisionTime(i, pos, vel, particle_radius, size_X, size_Y)
        index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        times_pw = np.insert(times_pw, index, new_entry, axis=0)
    else:
        j = int(j)
        # Particle-particle collision, recalculates entries involving i and j.
        times_pp = times_pp[~np.isin(times_pp, [i, j]).any(axis=1)]
        times_pw = times_pw[~np.isin(times_pw, [str(i), str(j)]).any(axis=1)]
        
        for a in range(n_particles):
            if (a==i and a!=(n_particles-1)): # Avoid i-i case
                a=a+1
            new_entry = detectCollisionTime(i, a, pos, vel, particle_radius)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        for a in range(n_particles):
            if ((a==j or a==i) and a!=n_particles-1): # Avoid j-j case and j-i case (already calculated)
                a=a+1
            new_entry = detectCollisionTime(j, a, pos, vel, particle_radius)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        
        times_pw_float = np.array([float(a) for a in times_pw[:,2]])
        
        # Wall update
        new_entry = detectWallCollisionTime(i, pos, vel, particle_radius, size_X, size_Y)
        new_entry_j = detectWallCollisionTime(j, pos, vel, particle_radius, size_X, size_Y)
        index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        index_j = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        times_pw = np.insert(times_pw, index, new_entry, axis=0)
        times_pw = np.insert(times_pw, index_j, new_entry_j, axis=0)
        
##################################################################################### unificar listas de tiempo en una sola
  
def computeNextCollision():
    """ Propagates particles until next collision and updates velocities 
        after it. Checks if next col. is particle-particle or particle-wall """
    global pos, vel
    t_pp = float(times_pp[0,2])
    t_pw = float(times_pw[0,2])
    # Check if particle-particle or particle-wall collision
    if t_pp <= t_pw:
        # Propagate particles until current collision
        propagate(t_pp, n_particles, particle_radius, size_X, size_Y, pos, vel)
        advanceTime(t_pp, times_pp, times_pw)
        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        # Compute change in velocities due to collision
        particleCollision(i, j, vel, pos, particle_radius)
        updateCollisionLists(t_pp, i, j)
    else:
        propagate(t_pw, n_particles, particle_radius, size_X, size_Y, pos, vel)
        advanceTime(t_pw, times_pp, times_pw)
        i = int(times_pw[0,0])
        wall = times_pw[0,1]
        wallCollision(i, wall, vel, restitution_coef)
        updateCollisionLists(t_pw, i)      

#times_pw = list(times_pw)    
# Here begins the actual script
pos = initRandomPos(particle_radius, n_particles, size_X, size_Y)
vel = initRandomVel(n_particles)
createWallCollisionList()
createCollisionList()
for c in range(n_collisions):
    computeNextCollision()
    saveData(c, data_folder, n_particles, pos, vel)
    print("Saving file for colission nº: " + str(c))