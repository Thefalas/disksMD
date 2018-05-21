# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:53:33 2018

@author: malopez
"""
import math
import numpy as np

#eps = 500*np.finfo(float).eps # Machine epsilon

def infIfNegative(t):
    #if t <= eps:
    if t <= 0:
        return 'inf'
    else:
        return t

def nanIfNegative(t):
    if t <= 0:
        return math.nan
    else:
        return t
    
#def deleteInfs(timesList):
#    timesList = timesList[~np.isin(timesList, ['inf']).any(axis=1)]
#    return timesList

def saveData(col_number, data_folder, n_particles, pos, vel):
    """ Saves the positions and velocities of every particle to an external
        file after current colision """
    file_name_pos = data_folder + "/xy"+'{0:05d}'.format(col_number)+".dat"
    #np.save(file_name_pos, pos)
    with open(file_name_pos,'w') as file:
        for i in range(n_particles):
            file.write('{0:10.2f} {1:10.2f}\n'.format(pos[i,0], pos[i,1]))
    file.closed
    
    file_name_vel = data_folder + "/vxvy"+'{0:05d}'.format(col_number)+".dat"
    #np.save(file_name_vel, vel)
    with open(file_name_vel,'w') as file:
        for i in range(n_particles):
            file.write('{0:10.2f} {1:10.2f}\n'.format(vel[i,0], vel[i,1]))
    file.closed
    
def readData(col_number, data_folder):
    file_name_vel = data_folder + "/vxvy"+'{0:05d}'.format(col_number)+".dat"
    velocities = np.loadtxt(file_name_vel)
    return velocities