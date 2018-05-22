# -*- coding: utf-8 -*-
"""
Created on Wed May 16 18:56:10 2018

@author: malopez
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from initialization import RandomGenerator
from tools import saveData
from statistics import velocityDistribution, computeKurtosis
from randomForce import KickGenerator
from eventLists import EventList
from eventEvaluator import EventEvaluator
from propagation import propagate

# ------ Settings ------

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 0.75 # TODO: This parameter is not working properly if !=1.0
particle_radius = 1.0
n_particles = 75 # 2 is the minimun number of particles
desired_collisions_per_particle = 100
n_collisions = n_particles*desired_collisions_per_particle
size_X = 30 # System size X
size_Y = 30 # System size Y
abs_time = 0.0 # Just to keep record of absolute time

baseKickIntensity = 850 # Posteriormente escalado por el dt de la siguiente colision
kick = True

verbose_kick = False
verbose_absTime = False
verbose_percent = False
verbose_temperature = True
verbose_saveData = False


# ------ Here begins the actual script ------
    
# Random initialization of position and velocity arrays
ranGen = RandomGenerator(particle_radius, n_particles, size_X, size_Y)
#vel = np.zeros((n_particles, 2), dtype=float)
vel = ranGen.initRandomVel()
pos = ranGen.initRandomPos()

# First calculation of next collisions, saving them in a Pandas DataFrame
# stored as an attribute 'eventTimesList' of the class 'EventList'
events = EventList(n_particles, particle_radius, size_X, size_Y)
events.updateEventList(pos, vel)
        
# Initialization of the Random Force (aka: kick) generator
kickGen = KickGenerator(n_particles, baseKickIntensity)

# Initialization of the Event Evaluator
evEval = EventEvaluator(restitution_coef, particle_radius)

# We open a file to store temperature data
file_name_temp = data_folder + "/t.dat"
os.remove(file_name_temp)
file_t  = open(file_name_temp,'a')      


# We call the main loop for every collision
for c in range(n_collisions):

    # First, we select the first element of the event list and check when it
    # is going to take place that next collision
    nextEvent = evEval.selectFirstEvent(events.eventTimesList)
    dt = evEval.getEventTime(nextEvent)

    # With this dt we can update the global time count, just to keep track of it
    abs_time += dt
    # Then we propagate particles (change positions) until that event
    pos = propagate(dt, pos, vel)
    # After that we change the velocities of involved particles by evaluating
    # that event
    vel = evEval.evaluateEvent(nextEvent, vel, pos)
    # When all this has finished we need to delete and recalculate the
    # event list (update it)    
    events.updateEventList(pos, vel)
    
    if kick == True:
        # Finally, we need to apply the random force (this part is optional)
        # Kicks and update collision times, since they must have changed
        vel = kickGen.randomKick(vel, abs_time)
        events.updateEventList(pos, vel)
        if verbose_kick == True:
            print('Kick! - Time since last one: ', kickGen.timeInterval, ' - Intensity: ', kickGen.kickIntensity)
    

    # Compute mean temperature for each step and save it to a file
    # together with the absolute time (to plot it later)
    temperature = vel*vel
    temperature = temperature[:,0] + temperature[:,1]
    meanTemperature = temperature.mean()
    if verbose_temperature == True:
        print('Temperature: '+'{:.2f}'.format(meanTemperature))
    file_t.write('{0:10.6f} {1:10.2f}\n'.format(abs_time, meanTemperature))

    
    
    if verbose_absTime == True:
        print('Contador de tiempo absoluto: ', str(abs_time))

    # We save positions and velocities data after current collision
    saveData(c, data_folder, n_particles, pos, vel)
    p = "{:.2f}".format(100*(c/n_collisions)) + " %" # Percent completed
    if verbose_percent == True:
        print(p)
    if verbose_saveData == True:
        print('Saving file, collision nº: '+str(c+1)+' / '+str(n_collisions))

# End of the simulation
print("Simulation finished, data can be found at: " + data_folder)
file_t.close()
        
# Now we print an histogram of the velocity distribution (in x and y direction)
h = velocityDistribution(n_collisions, data_folder)
k = computeKurtosis(n_collisions, data_folder)
print("--Kurtosis-- (3 for a Maxwellian distribution)")
print("Kurtosis for axis x is: ", "{:.2f}".format(k[0]))
print("Kurtosis for axis y is: ", "{:.2f}".format(k[1]))

# Read temperature data and plot it against time
t = np.loadtxt(file_name_temp)
#plt.plot(np.log10(t))
#plt.plot(t)
