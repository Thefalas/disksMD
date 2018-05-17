# -*- coding: utf-8 -*-
"""
Created on Wed May 16 18:52:50 2018

@author: malopez
"""
import numpy as np
from measure import distance, relativeVelocity
from tools import infIfNegative
    
class CollisionDetector():
    def __init__(self, pos, vel, particle_radius, size_X, size_Y):
        self.pos = pos
        self.vel = vel
        self.particle_radius = particle_radius
        self.size_X = size_X
        self.size_Y = size_Y
        
        # To be able to apply the 'computeCollisionTime' function to a Dataframe,
        # we need to first vectorize the function 'computeCollisionTime', as in:
        # https://es.stackoverflow.com/a/286
        # Although stored as an attribute, this can be used as a method of this
        # class in the main program
        self.computeCollisionTime_vectorized = np.vectorize(self.computeCollisionTime)
        
    
    def computeCollisionTime(self, first_element, second_element, eventType):
        if eventType == 'particleParticle_collision':
            dt = self.particleCollisionTime(first_element, second_element)
        elif eventType == 'particleWall_collision':
            dt = self.wallCollisionTime(first_element, second_element)            
        return dt
        
    
    def wallCollisionTime(self, first_element, second_element):
        """ Returns the time until particle i (first_element) hits a wall """
        x = self.pos[first_element, 0]
        y = self.pos[first_element, 1]
        vx = self.vel[first_element, 0]
        vy = self.vel[first_element, 1]
        
        if second_element == 'leftWall':
            if vx==0:
                t = 'inf'
            else:
                x_leftWall = 0.0
                t = infIfNegative((self.particle_radius + x_leftWall - x)/vx)
        elif second_element == 'rightWall':
            if vx==0:
                t = 'inf'
            else:
                x_rightWall = self.size_X
                t = infIfNegative((-self.particle_radius + x_rightWall - x)/vx)
        elif second_element == 'topWall':
            if vy==0:
                t = 'inf'
            else:
                y_topWall = self.size_Y
                t = infIfNegative((-self.particle_radius + y_topWall - y)/vy)
        elif second_element == 'bottomWall':
            if vy==0:
                t = 'inf'
            else:
                y_bottomWall = 0.0
                t = infIfNegative((self.particle_radius + y_bottomWall - y)/vy)
        return t
           

    def particleCollisionTime(self, first_element, second_element):
        """ Returns the time until the next collision between particles i, j """
        # Quantities required in following formula
        r = distance(first_element, second_element, self.pos)
        r2 = np.dot(r, r)
        v = relativeVelocity(first_element, second_element, self.vel)
        v2 = np.dot(v, v)
        b = np.dot(r, v)
        d = 2*self.particle_radius
        # We name 'inner_term' everything that will fall under the square root 
        inner_term = b*b - v2*(r2 - d*d)
        
        # We need to filter non-valid results
        if (inner_term<0 or v2<=0 or first_element==second_element):
            t = 'inf'
        else:
            # The following formula has been taken from Eq: 14.2.2 in
            # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
            t = (-b - np.sqrt(inner_term))/v2
            t = infIfNegative(t) # The collision ocurred in the past    
        return t
