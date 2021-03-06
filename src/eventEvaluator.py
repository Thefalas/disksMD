# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:09:16 2018

@author: malopez
"""
import numpy as np
from measure import distance, relativeVelocity

class EventEvaluator():
    def __init__(self, restitution_coef, inel_leftWall, inel_rightWall, 
                 inel_topWall, inel_bottomWall, particle_radius, size_X, size_Y):
        self.restitution_coef = restitution_coef
        self.inel_leftWall = inel_leftWall
        self.inel_rightWall = inel_rightWall
        self.inel_topWall = inel_topWall
        self.inel_bottomWall = inel_bottomWall
        self.particle_radius = particle_radius
        self.size_X = size_X
        self.size_Y = size_Y
        
        
    def selectFirstEvent(self, eventTimesList):
        """ Returns the first element of the events list as a single-row
            Pandas DataFrame """
        firstEvent = eventTimesList.iloc[0]
        return firstEvent
    
    
    def getEventTime(self, event):
        """ Returns the time 'dt' of an event as a float """
        t = float(event['dt'])
        return t
    
    
    def evaluateEvent(self, event, vel, pos):
        """ Checks the event type and decides what to do. For now, it updates
            the velocities array """
            
        if event.eventType == 'particleWall_collision':
            vel = self.wallCollision(event.first_element, event.second_element, vel)
            # vel = wallCollision(event['first_element'], event['second_element'], vel, self.restitution_coef)
        elif event.eventType == 'particleParticle_collision':
            vel = self.particleCollision(event.first_element, event.second_element, vel, pos)
            #vel = wallCollision(event['first_element'], event['second_element'], vel, pos, self.restitution_coef)
            
        return vel
    
    
    
    def wallCollision(self, i, wall, vel):
        #i = int(i)
        #wall = str(wall)

        if wall=='leftWall':
            vel[i,0] = -self.inel_leftWall * vel[i,0] # x component changes direction
        elif wall=='rightWall':
            vel[i,0] = -self.inel_rightWall * vel[i,0] # x component changes direction
        elif wall=='topWall':
            vel[i,1] = -self.inel_topWall * vel[i,1] # y component changes direction
        elif wall=='bottomWall':
            vel[i,1] = -self.inel_bottomWall * vel[i,1] # y component changes direction               
            
        return vel
    
    def particleCollision(self, i, j, vel, pos):
        #i = int(i)
        #j = int(j)
        
        r = distance(i, j, pos)
        v = relativeVelocity(i, j, vel)
        b = np.dot(r, v)
        # The following formula has been taken from Eq: 14.2.4 in
        # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
        delta_v = (-b/(4*self.particle_radius**2))*r
        # TODO: a mass parameter would be useful when expanding functionality
        vel[i] = self.restitution_coef*(vel[i] + delta_v)
        vel[j] = self.restitution_coef*(vel[j] - delta_v)    
        return vel