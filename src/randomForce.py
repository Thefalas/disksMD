# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:18:36 2018

@author: malopez
"""
import numpy as np

class KickGenerator():
    def __init__(self, n_particles, baseKickIntensity):
        self.n_particles = n_particles
        self.baseKickIntensity = baseKickIntensity
        # Time of last kick
        self.t_lastKick = 0
        
    def randomKick(self, vel, globalTime):
        # First, we calculate the time that has passed since last collision/kick
        timeInterval = globalTime - self.t_lastKick
        # The intensity of current kick is proportional to that time.
        # I.e: The longer since last kick the more intense this will be
        kickIntensity = self.baseKickIntensity * timeInterval
        # We apply the kick to the particles (normal distribution)
        # Intensity means std. dev. of the distribution
        vel = vel + np.random.normal(0, kickIntensity, vel.shape)
        # Updating the attribute for next call
        self.t_lastKick = globalTime
        print('Kick! - Time since last one: ', timeInterval, ' - Intensity: ', kickIntensity)
        
        return vel
        