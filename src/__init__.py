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
from statistics import velocityDistribution, computeKurtosis, computeExcessKurtosis_a2, computeKurtosisCustom
from randomForce import KickGenerator
from eventLists import EventList
from eventEvaluator import EventEvaluator
from propagation import propagate

# ------ Settings ------

#data_folder = "C:/Users/malopez/Desktop/disksMD/data"
data_folder = "../data"
restitution_coef = 0.55 # Energy lost in particle-particle collisions

# If the system is periodic, its 'effective size' may be a little bigger (a diameter in each dimension)
periodicWalls = False # True if all walls are periodic (a particle would appear on the opposite wall)
periodicSideWalls = False # True if, only left and right walls are periodic

# Inelasticity coefficients for the different walls
inel_leftWall =1.0 
inel_rightWall = 1.0
inel_topWall = 1.0
inel_bottomWall = 1.0

particle_radius = 1.0
n_particles = 300 # 2 is the minimun number of particles
desired_collisions_per_particle = 15
n_collisions = n_particles*desired_collisions_per_particle
size_X = 100 # System size X
size_Y = 100 # System size Y
abs_time = 0.0 # Just to keep record of absolute time
baseStateVelocity = 0.7 # Used to initialize the velocities array, std. dev.

baseKickIntensity = 0.2 # This value will then be scaled by the time interval between collisions
kick = True
stepsBetweenKicks = 20 # Number of collisions between two kicks

verbose_kick = False
verbose_debug = False
verbose_absTime = False
verbose_percent = False
verbose_temperature = True
verbose_saveData = False


# ------ Here begins the actual script ------
    
# Random initialization of position and velocity arrays
ranGen = RandomGenerator(particle_radius, n_particles, size_X, size_Y, baseStateVelocity)
#vel = np.zeros((n_particles, 2), dtype=float)
vel = ranGen.initRandomVel()
pos = ranGen.initRandomPos()

# First calculation of next collisions, saving them in a Pandas DataFrame
# stored as an attribute 'eventTimesList' of the class 'EventList'
events = EventList(n_particles, particle_radius, size_X, size_Y, periodicWalls, periodicSideWalls)
events.updateEventList(pos, vel)
        
# Initialization of the Random Force (aka: kick) generator
kickGen = KickGenerator(n_particles, baseKickIntensity)

# Initialization of the Event Evaluator
evEval = EventEvaluator(restitution_coef, periodicWalls, periodicSideWalls, 
                        inel_leftWall, inel_rightWall, inel_topWall, 
                        inel_bottomWall, particle_radius, size_X, size_Y)

# We open a file to store temperature and excess kurtosis (a2) data
file_name_temp = data_folder + '/t_alpha'+str(restitution_coef)+'.dat'
file_name_a2 = data_folder + '/a2_alpha'+str(restitution_coef)+'.dat'
try:
    os.remove(file_name_temp)
    os.remove(file_name_a2)
except:
    pass
file_t  = open(file_name_temp,'a') 
file_a2  = open(file_name_a2,'a')     


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
    
    if (kick == True and c%stepsBetweenKicks==0):
        # Finally, we need to apply the random force (this part is optional)
        # Kicks and update collision times, since they must have changed
        vel = kickGen.randomKick(vel, abs_time)
        #events.updateEventList(pos, vel)
        if verbose_kick == True:
            print('Kick! - Time since last one: ', kickGen.timeInterval, ' - Intensity: ', kickGen.kickIntensity)
    
    # When all this has finished we need to delete and recalculate the
    # event list (update it)    
    events.updateEventList(pos, vel)

    # Compute mean temperature for each step and save it to a file
    # together with the absolute time (to plot it later)
    v2_sep = vel*vel
    v2 = v2_sep[:,0] + v2_sep[:,1]
    meanTemperature = v2.mean()
    kurtosis = computeKurtosisCustom(vel)
    a2 = computeExcessKurtosis_a2(kurtosis, 2)
    if verbose_temperature == True:
        print('Temperature: '+'{:.3f}'.format(meanTemperature))
        #print('{:.3f}'.format(a2))
    # Saving temperature and a2 data
    file_t.write('{0:10.6f} {1:10.4f}\n'.format(abs_time, meanTemperature))
    file_a2.write('{0:10.6f} {1:10.4f}\n'.format(abs_time, a2))
    
    
    if verbose_absTime == True:
        print('Contador de tiempo absoluto: ', str(abs_time))


    # We save positions and velocities data after current collision
    saveData(c, data_folder, n_particles, pos, vel)
    p = "{:.2f}".format(100*(c/n_collisions)) + " %" # Percent completed
    if verbose_percent == True:
        print(p)
    if verbose_saveData == True:
        print('Saving file, collision nº: '+str(c+1)+' / '+str(n_collisions))
      
        
        
        
    if verbose_debug == True:
        print(' ')
        print('COLLISION Nº: '+str(c))
        print('Event list head:')
        print(events.eventTimesList.iloc[0:1])
        if dt==0:
            print('---------------------- DOUBLE COLLISION DUE TO RANDOM KICK (OVERLAP AVOIDED) ----------------------')      
        try:
            print('Positions, particles '+str(nextEvent['first_element'])+' and '+str(nextEvent['second_element']))
            print(pos[nextEvent['first_element']], pos[nextEvent['second_element']])
            print('Velocities, particles '+str(nextEvent['first_element'])+' and '+str(nextEvent['second_element']))
            print(vel[nextEvent['first_element']], vel[nextEvent['second_element']])  
        except:
            print('Position, particle '+str(nextEvent['first_element']))
            print(pos[nextEvent['first_element']])
            print('Velocity, particle '+str(nextEvent['first_element']))
            print(vel[nextEvent['first_element']]) 




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
#fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
#ax.set_xlim(0, n_collisions)
#plt.plot(np.log10(t))
#plt.plot(t)
