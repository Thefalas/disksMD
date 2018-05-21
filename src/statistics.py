# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:33:47 2018

@author: malopez
"""
import numpy as np
from scipy.stats import kurtosis
import matplotlib.pyplot as plt
import seaborn
from tools import readData

def getStationaryState(n_collisions, data_folder):
    """ Here we read the last 75 % of the data and return those velocities """
    # First, we need to read the data from the simulation
    velocities = []
    for a in range(n_collisions):
        result = readData(a, data_folder)
        velocities.append(result)
    
    # Taking the last 20% of collisions and saving them in an array
    last75 = int(75*n_collisions/100)
    vel = velocities[n_collisions-1][:,:]
    for a in range(last75):
        current = velocities[(n_collisions-2)-a][:,:]
        tup = (vel, current)
        vel = np.vstack(tup)
    return vel

def velocityDistribution(n_collisions, data_folder):
    """ This function returns an histogram plot of the velocity distribution of
        particles, the last 75% of total collisions are used for this """
    # First, we need to read the data from the simulation
    vel = getStationaryState(n_collisions, data_folder)       
#    velX = vel[:,0]
#    velY = vel[:,1] 
#    h = np.histogram(vel)
#    h2 = np.hstack(h)
    seaborn.set_style('whitegrid')
    seaborn.kdeplot(vel[:,0], bw=0.5)
    # With former array vel we can plot two histograms (for x and y directions)
    #b = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    #histPlot = plt.hist(vel, density=True, bins=b)
    histPlot = plt.hist(vel, density=True, bins='auto')
    # Another interesting visualization
#    histPlot2D = plt.hist2d(vel[:,0], vel[:,1], bins=b)
    return histPlot

def computeKurtosis(n_collisions, data_folder):
    # First, we need to read the data from the simulation
    vel = getStationaryState(n_collisions, data_folder)
    k = kurtosis(vel, fisher=False)
    return k