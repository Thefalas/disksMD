"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
import numpy as np
from initialization import initRandomPos, initRandomVel
from tools import saveData
from collision import wallCollision, particleCollision
from propagation import propagate, advanceTime
from timeLists import createCollisionList, createWallCollisionList, updateCollisionLists

eps = 5000*np.finfo(float).eps # Machine epsilon

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 1.0
particle_radius = 1.0
n_particles = 5
desired_collisions_per_particle = 50
n_collisions = n_particles*desired_collisions_per_particle

scale_factor = 25
form_factor = 16/9

size_X = scale_factor*particle_radius
size_Y = scale_factor*particle_radius/form_factor
        
##################################################################################### unificar listas de tiempo en una sola
  
def computeNextCollision():
    """ Propagates particles until next collision and updates velocities 
        after it. Checks if next col. is particle-particle or particle-wall """
    global pos, vel, times_pp, times_pw
    t_pp = float(times_pp[0,2])
    t_pw = float(times_pw[0,2])
    # Check if particle-particle or particle-wall collision
    if t_pp <= t_pw:
        # Propagate particles until current collision
        propagate(t_pp, n_particles, particle_radius, size_X, size_Y, pos, vel)
        advanceTime(t_pp-eps, times_pp, times_pw)
        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        # Compute change in velocities due to collision
        particleCollision(i, j, vel, pos, particle_radius)
        times_pp=updateCollisionLists(t_pp, n_particles, particle_radius, size_X, size_Y, pos, vel, times_pp, times_pw, i, j)[0]
        times_pw=updateCollisionLists(t_pp, n_particles, particle_radius, size_X, size_Y, pos, vel, times_pp, times_pw, i, j)[1]
    else:
        propagate(t_pw, n_particles, particle_radius, size_X, size_Y, pos, vel)
        advanceTime(t_pw-eps, times_pp, times_pw)
        i = int(times_pw[0,0])
        wall = str(times_pw[0,1])
        wallCollision(i, wall, vel, restitution_coef)
        times_pp=updateCollisionLists(t_pw, n_particles, particle_radius, size_X, size_Y, pos, vel, times_pp, times_pw, i, j='none')[0]
        times_pw=updateCollisionLists(t_pw, n_particles, particle_radius, size_X, size_Y, pos, vel, times_pp, times_pw, i, j='none')[1]

#times_pw = list(times_pw)    
# Here begins the actual script
pos = initRandomPos(particle_radius, n_particles, size_X, size_Y)
vel = initRandomVel(n_particles)
times_pw = createWallCollisionList(n_particles, particle_radius, size_X, size_Y, pos, vel)
times_pp = createCollisionList(n_particles, particle_radius, pos, vel)

for c in range(n_collisions):
    computeNextCollision()
    saveData(c, data_folder, n_particles, pos, vel)
    print("Saving file for colission nº: " + str(c))