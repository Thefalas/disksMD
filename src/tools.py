# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:53:33 2018

@author: malopez
"""
import math

def infIfNegative(t):
    if t <= 0:
        return 'inf'
    else:
        return t

def nanIfNegative(t):
    if t <= 0:
        return math.nan
    else:
        return t

def saveData(col_number, data_folder, n_particles, pos, vel):
    """ Saves the positions and velocities of every particle to an external
        file after current colision """
    file_name_pos = data_folder + "/xy"+'{0:04d}'.format(col_number)+".dat"
    with open(file_name_pos,'w') as file:
        for i in range(n_particles):
            file.write('{0:10.2f} {1:10.2f}\n'.format(pos[i,0], pos[i,1]))
    file.closed
    
    file_name_vel = data_folder + "/vxvy"+'{0:04d}'.format(col_number)+".dat"
    with open(file_name_vel,'w') as file:
        for i in range(n_particles):
            file.write('{0:10.2f} {1:10.2f}\n'.format(vel[i,0], vel[i,1]))
    file.closed