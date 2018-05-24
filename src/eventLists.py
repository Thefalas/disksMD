# -*- coding: utf-8 -*-
"""
Created on Wed May 16 12:39:55 2018

@author: malopez
"""
import math
import numpy as np
import pandas as pd
from collisionTimes import CollisionDetector
from measure import MeasureClass

n_particles = 50

class EventList():    
    def __init__(self, n_particles, particle_radius, size_X, size_Y, periodicWalls, periodicSideWalls):
        self.n_particles = n_particles
        self.particle_radius = particle_radius
        self.size_X = size_X
        self.size_Y = size_Y
        self.periodicWalls = periodicWalls
        self.periodicSideWalls = periodicSideWalls
        
        # We  will init this attribute (the event times list itself) outside 
        # the class definition, by calling the 'updateEventList' function
        self.eventTimesList = self.initEventList()

        
    def updateEventList(self, pos, vel):            
        # We calculate collision times (from position and speed data)
        # and fill the list previously initialized (self.eventTimesList)
        evTimes = self.fillList(self.eventTimesList, pos, vel)
        # After that we order the list by 'dt' in ascending order
        evTimes = self.orderList(evTimes)
        
        # We save the list as an attribute of the class
        self.eventTimesList = evTimes

        
    def initEventList(self):
        part_i = pd.DataFrame(np.arange(self.n_particles, dtype=np.int32), 
                              columns=('first_element',))
        wallLeft = pd.DataFrame(np.full((self.n_particles,), 'leftWall'), 
                            columns=('second_element',))
        wallRight = pd.DataFrame(np.full((self.n_particles,), 'rightWall'), 
                            columns=('second_element',))
        wallTop = pd.DataFrame(np.full((self.n_particles,), 'topWall'), 
                            columns=('second_element',))
        wallBottom = pd.DataFrame(np.full((self.n_particles,), 'bottomWall'), 
                            columns=('second_element',))
        dt = pd.DataFrame(np.zeros((self.n_particles, ), dtype=np.float64), 
                          columns=('dt',))
        eventType = pd.DataFrame(np.full((self.n_particles,), 'particleWall_collision'), 
                                 columns=('eventType',))
        
        wallTimesList_left = pd.concat((part_i, wallLeft, dt, eventType), axis=1)
        wallTimesList_right = pd.concat((part_i, wallRight, dt, eventType), axis=1)
        wallTimesList_top = pd.concat((part_i, wallTop, dt, eventType), axis=1)
        wallTimesList_bottom = pd.concat((part_i, wallBottom, dt, eventType), axis=1)
        # Creating an empty Pandas dataframe to store collision times for
        # particle-wall collisions        
        wallTimesList = pd.concat((wallTimesList_left, wallTimesList_right, 
                                   wallTimesList_top, wallTimesList_bottom), axis=0)
        
        
        # The number of elements in particle-particle collision list is
        # factorial(n)/(2*factorial(n-2)) where n=n_particles
        # This is without repetition (we don't save (3,7) and (7,3); or (5,5) i.e).
        # http://mathworld.wolfram.com/Permutation.html
        n = int(math.factorial(self.n_particles)/(2*math.factorial(self.n_particles-2)))
        
        part_i = pd.DataFrame(np.zeros((n, ), dtype=np.int32), 
                              columns=('first_element',))
        part_j = pd.DataFrame(np.zeros((n, ), dtype=np.int32), 
                              columns=('second_element',))
        
        a = 0
        for i in range(self.n_particles):
            for j in range(i+1, (self.n_particles)):
                part_i.values[a] = i
                part_j.values[a] = j
                a = a+1
            
        dt = pd.DataFrame(np.zeros((n, ), dtype=np.float64), 
                          columns=('dt',))
        eventType = pd.DataFrame(np.full((n,), 'particleParticle_collision'), 
                                 columns=('eventType',))
        # Creating an empty Pandas dataframe to store collision times for
        # particle-particle collisions
        particleTimesList = pd.concat((part_i, part_j, dt, eventType), axis=1)
        
        # Joining those two lists into a more general 'events' list.
        times = pd.concat((wallTimesList, particleTimesList), axis=0)
        return times
 
       
    def fillList(self, times, pos, vel):
        # TODO: We create an instance of measure class, to measure distances
        # and rel. velocities so that collision times can be calculated.
        # This is done this way to avoid passing pos and vel arrays many times
        measureObject = MeasureClass(pos, vel)
        # We create an instance of 'CollisionDetector'
        #colDetector = CollisionDetector(pos, vel, self.particle_radius, self.size_X, self.size_Y)
        colDetector = CollisionDetector(measureObject, pos, vel, self.particle_radius, 
                                        self.size_X, self.size_Y, self.periodicWalls, self.periodicSideWalls)
        # Given any pair of elements, compute collision times between them
        # Computing time is minimized following the advice in:
        # https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6
        # We use a vectorizez version of the function 'computeCollisionTime'
        # This way we don't need to loop over the DataFrame and we can 
        # calculate collision times in a vectorized way (much faster)
        times['dt'] = colDetector.computeCollisionTime_vectorized(times['first_element'].values, times['second_element'].values, times['eventType'].values)
        return times
    
    
    def orderList(self, times):
        # Sort the DataFrame by 'dt', ascendig order
        
        # Without the next line, ordering doesn't work properly, it confuses
        # the type of dt column, considering it a string and not sorting right
        times['dt'] = times['dt'].astype('float64') 
        
        times = times.sort_values('dt')
        return times
    

    #def advanceListTimes(self, t):
     #   """ Advances al times in the event list a quantity 't' """
      #  self.eventTimesList['dt'] = self.eventTimesList['dt'] - t