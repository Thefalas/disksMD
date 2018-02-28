# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:10:28 2018

@author: malopez
"""
import math
import numpy as np
from measure import distance, relativeVelocity
from tools import nanIfNegative, infIfNegative

eps = 5000*np.finfo(float).eps # Machine epsilon

def detectCollisionTime(i, j, pos, vel, particle_radius):
    """ Returns the time until the next collision between particles i, j """
    i = int(i)
    j = int(j)
    
    r = distance(i, j, pos)
    r2 = np.dot(r, r)
    v = relativeVelocity(i, j, vel)
    v2 = np.dot(v, v)
    b = np.dot(r, v)
    d = 2*particle_radius
    
    inner_term = b*b - v2*(r2 - d*d)
    if inner_term<0:
        t = 'inf'
    else:
        # The following formula has been taken from Eq: 14.2.2 in
        # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
        t = (-b - math.sqrt(inner_term))/(v2+eps) # or (v2+eps)
        t = infIfNegative(t) # The collision ocurred in the past

    part_i = np.array([i])
    part_j = np.array([j])
    dt = np.array([t]) 
    times_pp = np.stack((part_i, part_j, dt), axis=1)
    return times_pp
    
def detectWallCollisionTime(i, pos, vel, particle_radius, size_X, size_Y):
    """ Returns the time until particle i hits a wall """
    i = int(i)

    x = pos[i, 0]
    y = pos[i, 1]
    vx = vel[i, 0]
    vy = vel[i, 1]
    
    x_leftWall = 0.0
    x_rightWall = size_X
    y_topWall = size_Y
    y_bottomWall = 0.0

    t_left = nanIfNegative((particle_radius + x_leftWall - x)/vx) #or (vx+eps)
    t_right = nanIfNegative((-particle_radius + x_rightWall - x)/vx)
    t_top = nanIfNegative((-particle_radius + y_topWall - y)/vy)
    t_bottom = nanIfNegative((particle_radius + y_bottomWall - y)/vy)
    
    """t_left = [t_left, "left"]
    t_right = [t_right, "left"]
    t_top = [t_top, "left"]
    t_bottom = [t_bottom, "left"]
    
    times = sorted([t_left, t_right, t_top, t_bottom], key=itemgetter(0) )"""
    
    part_i = np.array([i for a in range(4)])
    wall = np.array(['left', 'right', 'top', 'bottom'])
    dt = np.array([t_left, t_right, t_top, t_bottom])
    
    times_pw = np.stack((part_i, wall, dt), axis=1)
    # We need to sort the list in order to return only the element 
    # with the lowest collision time. This approach is similar to the
    # one found at: https://stackoverflow.com/a/2828121
    # More complex cause float conversion is needed for times column in array.
    times_pw = times_pw[np.array([float(a) for a in times_pw[:,2]]).argsort()]
    # We need to reshape to return a 2D array, although with just one row
    return times_pw[0].reshape(1,-1)
