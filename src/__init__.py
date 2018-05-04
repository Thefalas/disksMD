# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
import numpy as np
from mpi4py import MPI
from initialization import RandomGenerator
from tools import saveData
from timeLists import createCollisionList, createWallCollisionList
from mainLoop import computeNextCollision
from statistics import velocityDistribution, computeKurtosis
from randomForce import randomKick

# Settings
data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 1.0 # TODO: This parameter is not working properly if !=1.0
mu = 0.95 # Dynamic friction coef.
particle_radius = 1.0
n_particles = 50 # TODO: Why 3 is the minimun number of particles?
desired_collisions_per_particle = 10
n_collisions = n_particles*desired_collisions_per_particle
size_X = 30 # System size X
size_Y = 30 # System size Y
abs_time = 0.0 # Just to keep record of absolute time

kickIntensity = 1 #Escalado poorr el dt de la siguiente colision
interval_RK = 10
# A random kick will affect some particles every 10 collisions 
# We create a list to store which are those collisions
stepsRandomKick = np.arange(n_collisions/interval_RK, dtype=int)*interval_RK

# We get the numbre of processes over whitch computation will be spread
comm = MPI.COMM_WORLD
comm_size = comm.Get_size() # Gives number of ranks in comm
print('Number of processors: ', comm_size)
rank = comm.Get_rank()


# ---- Here begins the actual script ----

if comm_size > 1:
    # If possible we spread the computation of pos/vel over procceses/ranks
    
    # Random initialization of position and velocity arrays
    # Rank 1 will init velocities and send them to Rank 0 wich will init
    # positions and wait until receiving velocities.
    if rank == 1:
        print('Rank: ',rank, ', Inicializando velocidades')
        ranGen = RandomGenerator(particle_radius, n_particles, size_X, size_Y)
        vel = ranGen.initRandomVel()
        comm.send(vel, dest=0, tag=15)
        pos = comm.recv(source=0, tag=16)
        # First calculation of next collisions, saving them in two arrays
        print('Rank: ',rank, ', Calculando colisiones particula-particula')
        times_pp = createCollisionList(n_particles, particle_radius, pos, vel)
        comm.send(times_pp, dest=0, tag=17)
    if rank == 0:
        print('Rank: ',rank, ', Inicializando posiciones')
        ranGen = RandomGenerator(particle_radius, n_particles, size_X, size_Y)
        pos = ranGen.initRandomPos()
        vel = comm.recv(source=1, tag=15)
        comm.send(pos, dest=1, tag=16)
        # First calculation of next collisions, saving them in two arrays
        print('Rank: ',rank, ', Calculando colisiones particula-pared')
        times_pw = createWallCollisionList(n_particles, particle_radius, 
                                           size_X, size_Y, pos, vel)
        times_pp = comm.recv(source=1, tag=17)
        
    # The first procces (rank 0) will be in charge of the main loop
    if rank == 0:
        
        # We call the main loop for every collision
        for c in range(n_collisions):
            # Check if Random Kick affects this collision
            if c in stepsRandomKick:
                # Kick and update collision times, since they must have changed
                vel = randomKick(n_particles, vel, kickIntensity)
                times_pw = createWallCollisionList(n_particles, particle_radius, 
                                                   size_X, size_Y, pos, vel)
                times_pp = createCollisionList(n_particles, particle_radius, pos, vel)
                
            
            # Propagates, advances time, changes velocities and updates lists
            pos, vel, times_pp, times_pw, abs_time = computeNextCollision(n_particles, 
                                                                          particle_radius, 
                                                                          mu, 
                                                                          size_X, 
                                                                          size_Y, 
                                                                          restitution_coef, 
                                                                          pos, vel, 
                                                                          times_pp, times_pw, 
                                                                          abs_time)
            # The output from the function above is in the form of a tuple, we have
            # to extract the values of the four main arrays

            print('Contador de tiempo absoluto: ', str(abs_time))
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




else:
    # This is the usual way of doing things, just one procces
    
    # Random initialization of position and velocity arrays
    ranGen = RandomGenerator(particle_radius, n_particles, size_X, size_Y)
    pos = ranGen.initRandomPos()
    vel = ranGen.initRandomVel()
    # First calculation of next collisions, saving them in two arrays
    times_pw = createWallCollisionList(n_particles, particle_radius, size_X, 
                                       size_Y, pos, vel)
    times_pp = createCollisionList(n_particles, particle_radius, pos, vel)
    
    # We call the main loop for every collision
    for c in range(n_collisions):
        # Check if Random Kick affects this collision
        """if c in stepsRandomKick:
            # Kick and update collision times, since they must have changed
            vel = randomKick(n_particles, vel, kickIntensity)
            times_pw = createWallCollisionList(n_particles, particle_radius, 
                                                   size_X, size_Y, pos, vel)
            times_pp = createCollisionList(n_particles, particle_radius, pos, vel)"""
        
        
        # Propagates, advances time, changes velocities and updates lists
        pos, vel, times_pp, times_pw, abs_time = computeNextCollision(n_particles, 
                                                                      particle_radius, 
                                                                      mu, 
                                                                      size_X, 
                                                                      size_Y, 
                                                                      restitution_coef, 
                                                                      pos, vel, 
                                                                      times_pp, times_pw, 
                                                                      abs_time)
        # The output from the function above is in the form of a tuple, we have
        # to extract the values of the four main arrays
        
        print('Contador de tiempo absoluto: ', str(abs_time))
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
