# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:09:16 2018

@author: malopez
"""
import numpy as np
from measure import distance, relativeVelocity

class EventEvaluator():
    def __init__(self, restitution_coef, particle_radius):
        self.restitution_coef = restitution_coef
        self.particle_radius = particle_radius
        
        
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
            vel = wallCollision(event.first_element, event.second_element, vel, self.restitution_coef)
            # vel = wallCollision(event['first_element'], event['second_element'], vel, self.restitution_coef)
        elif event.eventType == 'particleParticle_collision':
            vel = particleCollision(event.first_element, event.second_element, vel, pos, self.particle_radius, self.restitution_coef)
            #vel = wallCollision(event['first_element'], event['second_element'], vel, pos, self.restitution_coef)
            
        return vel
    
    
    
def wallCollision(i, wall, vel, restitution_coef):
    i = int(i)
    wall = str(wall)

    if (wall=='leftWall' or wall=='rightWall'):
        vel[i,0] = -restitution_coef * vel[i,0] # x component changes direction
    elif (wall=='topWall' or wall=='bottomWall'):
        vel[i,1] = -restitution_coef * vel[i,1] # y component changes direction
    return vel

def particleCollision(i, j, vel, pos, particle_radius, restitution_coef):
    i = int(i)
    j = int(j)
    
    r = distance(i, j, pos)
    v = relativeVelocity(i, j, vel)
    b = np.dot(r, v)
    # The following formula has been taken from Eq: 14.2.4 in
    # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
    delta_v = (-b/(4*particle_radius*particle_radius))*r
    # TODO: a mass parameter would be useful when expanding functionality
    vel[i] = restitution_coef*(vel[i] + delta_v)
    vel[j] = restitution_coef*(vel[j] - delta_v)    
    return vel