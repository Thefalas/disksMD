"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
from initialization import initRandomPos, initRandomVel
from tools import saveData
from timeLists import createCollisionList, createWallCollisionList
from mainLoop import computeNextCollision
from statistics import velocityDistribution, computeKurtosis

# Settings
data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 1.0 # TODO: This parameter is not working properly if !=1.0
mu = 0.95 # Dynamic friction coef.
particle_radius = 1.0
n_particles = 20 # TODO: Why 3 is the minimun number of particles?
desired_collisions_per_particle = 100
n_collisions = n_particles*desired_collisions_per_particle
size_X = 20
size_Y = 20
abs_time = 0.0 # Just to keep record of absolute time

# Here begins the actual script
# Random initialization of position and velocity arrays
pos = initRandomPos(particle_radius, n_particles, size_X, size_Y)
vel = initRandomVel(n_particles)
# First calculation of next collisions, saving them in two arrays
times_pw = createWallCollisionList(n_particles, particle_radius, size_X, 
                                   size_Y, pos, vel)
times_pp = createCollisionList(n_particles, particle_radius, pos, vel)

# We call the main loop for every collision
for c in range(n_collisions):
    # Propagates, advances time, changes velocities and updates lists
    result = computeNextCollision(n_particles, particle_radius, mu, size_X, 
                                  size_Y, restitution_coef, pos, vel, 
                                  times_pp, times_pw, abs_time)
    # The output from the function above is in the form of a tuple, we have
    # to extract the values of the four main arrays
    pos = result[0]
    vel = result[1]
    times_pp = result[2]
    times_pw = result[3]
    abs_time = result[4]
    print(str(abs_time))
#    print(times_pp)
#    print(times_pw)
    # We save positions and velocities data after current collision
    saveData(c, data_folder, n_particles, pos, vel)
    p = "{:.2f}".format(100*(c/n_collisions)) + " %" # Percent completed
    print(p+" - Saving file, collision nº: "+str(c+1)+" / "+str(n_collisions))
# End of the simulation
print("Simulation finished, data can be found at: " + data_folder)

# Now we print an histogram of the velocity distribution (in x and y direction)
h = velocityDistribution(n_collisions, data_folder)
k = computeKurtosis(n_collisions, data_folder)
print("--Kurtosis-- (3 for a Maxwellian distribution)")
print("Kurtosis for axis x is: ", "{:.2f}".format(k[0]))
print("Kurtosis for axis y is: ", "{:.2f}".format(k[1]))