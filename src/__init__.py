"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
#TODO: Comentar mas todo el proceso ----------------------------------------------------------
from initialization import initRandomPos, initRandomVel
from tools import saveData
from timeLists import createCollisionList, createWallCollisionList
from mainLoop import computeNextCollision
from tools import deleteInfs

# Settings
data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 1.0
particle_radius = 1.0
n_particles = 5 #por que minimo 3?
desired_collisions_per_particle = 10
n_collisions = n_particles*desired_collisions_per_particle
size_X = 20
size_Y = 15

# Here begins the actual script
# Random initialization of postitios and velocities arrays
pos = initRandomPos(particle_radius, n_particles, size_X, size_Y)
vel = initRandomVel(n_particles)
# First calculation of next collisions, saving them in two arrays
times_pw = createWallCollisionList(n_particles, particle_radius, size_X, 
                                   size_Y, pos, vel)
times_pp = createCollisionList(n_particles, particle_radius, pos, vel)
# It is a good idea to delete imposible values to reduce the size of the list
times_pp = deleteInfs(times_pp)

# We call the main loop for every collision
for c in range(n_collisions):
    # Propagates, advances time, changes velocities and updates lists
    result = computeNextCollision(n_particles, particle_radius, size_X, 
                                  size_Y, restitution_coef, pos, vel, 
                                  times_pp, times_pw)
    # The output from the function above is in the form of a tuple, we have
    # to extract the values of the four main arrays
    pos = result[0]
    vel = result[1]
    times_pp = result[2]
    times_pw = result[3]
    print(times_pp)
    print(times_pw)
    # We save positions and velocities data after current collision
    saveData(c, data_folder, n_particles, pos, vel)
    print("Saving file for colission nº: "+str(c+1)+" / "+str(n_collisions))
# End of the simulation
print("Simulation finished, data can be found in: " + data_folder)