"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
import math
import random
import bisect
from operator import itemgetter, attrgetter
import numpy as np

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
eps = 5000*np.finfo(float).eps #Machine epsilon

restitution_coef = 1.0
particle_radius = 1.0
n_particles = 30
desired_collisions_per_particle = 50
n_collisions = n_particles*desired_collisions_per_particle

scale_factor = 80
form_factor = 16/9

size_X = scale_factor*particle_radius
size_Y = scale_factor*particle_radius/form_factor

pos_X = np.array([0.0 for i in range(n_particles)])
pos_Y = np.array([0.0 for i in range(n_particles)])
# Initialize particle positions as a 2D numpy array.
pos = np.stack((pos_X, pos_Y), axis=1)

vel_X = np.array([random.uniform(-5, 5) for i in range(n_particles)])
vel_Y = np.array([random.uniform(-5, 5) for i in range(n_particles)])
# Initialize particle velocities as a 2D numpy array.
vel = np.stack((vel_X, vel_Y), axis=1) #Deberia ser una dist gaussiana

# Initialize two arrays for storing particle-particle and particle-wall
# collision times; apart from time t, they save the indexes of interacting
# particles and/or the name of interacting wall.
part_i = np.array([0 for i in range(n_particles)])
dt = np.array([0.0 for i in range(n_particles)])
wall = np.array(['test' for i in range(n_particles)])

times_pw = np.stack((part_i, wall, dt), axis=1)
# The number of elements in particle-particle collision list is
# factorial(n)/(2*factorial(n-2)) where n=n_particles
# This is without repetition (we don't save (3,7) and (7,3); or (5,5) i.e).
# http://mathworld.wolfram.com/Permutation.html
pp_elements = int(math.factorial(n_particles)/(2*math.factorial(n_particles-2)))
part_i = np.array([0 for i in range(pp_elements)])
part_j = np.array([0 for i in range(pp_elements)])
dt = np.array([0.0 for i in range(pp_elements)])

times_pp = np.stack((part_i, part_j, dt), axis=1)

def initializeRandom():
    """ Initializes particle positions and velocities, makes sure that
        no particles overlap """
    global pos_X, pos_Y, vel_X, vel_Y, pos, vel
    # Reduced sizes so that particles are not generated inside walls
    reduc_size_X = size_X - particle_radius
    reduc_size_Y = size_Y - particle_radius
    # First particle is generated in a random position.
    pos_X[0] = random.uniform(0+particle_radius, reduc_size_X)
    pos_Y[0] = random.uniform(0+particle_radius, reduc_size_Y)
    # From 2nd particle we need to check if it overlaps with previous ones.
    for i in range(1, n_particles):
       overlap = False
       # While the distance is greater than 2 radius, generates new particles.
       while overlap==False:
           pos_X[i] = random.uniform(0+particle_radius, reduc_size_X)
           pos_Y[i] = random.uniform(0+particle_radius, reduc_size_Y)
           # Checking that it doesn't overlap with existent particles.
           for j in range(0, i):
               overlap = (distanceModulus(i, j) > 2*particle_radius)
               if overlap==False:
                  break
    pos = np.stack((pos_X, pos_Y), axis=1)
    
    vel_X = np.array([random.uniform(-5, 5) for i in range(n_particles)])
    vel_Y = np.array([random.uniform(-5, 5) for i in range(n_particles)])
    # Initialize particle velocities as a 2D numpy array.
    vel = np.stack((vel_X, vel_Y), axis=1) #Deberia ser una dist gaussiana
    
def distance(i, j):
    """ Returns the distance between two particles i, j as a numpy array """
    i = int(i)
    j = int(j)
    dist = pos[i] - pos[j]
    return dist

def distanceModulus(i, j):
    """ Measures the distance modulus between two particles i, j """
    i = int(i)
    j = int(j)
    dist_X = pos_X[j] - pos_X[i]
    dist_Y = pos_Y[j] - pos_Y[i]
    dist = math.sqrt(dist_X*dist_X + dist_Y*dist_Y)
    return dist

def relativeVelocity(i, j):
    """ Measures the relative velocity between two particles i, j """
    i = int(i)
    j = int(j)
    rel_v = vel[i] - vel[j]
    return rel_v

def infIfNegative(t):
    if t <= 0:
        return 'inf'
    else:
        return t

def nanIfNegative(t):
    if t < 0:
        return math.nan
    else:
        return t

def propagate(t):
    global pos, vel, times_pp, times_pw
    """ Updates positions for all particles, lineal movement during a time t.
        Modifies the lists containig collision times to reflect the time that
        has passed since last collision """
    # Reduced by a smolle amount to avoid singularity problems
    #t=t-eps
    for i in range(n_particles):
        pos[i] = pos[i] + vel[i]*t
        if pos[i,0] == particle_radius:
            pos[i,0] = pos[i,0] + eps
        elif pos[i,0] == size_X-particle_radius:
            pos[i,0] = pos[i,0] - eps
        elif pos[i,1] == particle_radius:
            pos[i,1] = pos[i,1] + eps
        elif pos[i,1] == size_Y-particle_radius:
            pos[i,1] = pos[i,1] - eps
    # Advances all entries a time t (time since last collision)
    times_pp[:,2] = times_pp[:,2] - t
    times_pw[:,2] = np.array([float(a) for a in times_pw[:,2]]) - t
    
def detectCollisionTime(i, j):
    """ Returns the time until the next collision between particles i, j """
    i = int(i)
    j = int(j)
    
    r = distance(i, j)
    r2 = np.dot(r, r)
    v = relativeVelocity(i, j)
    v2 = np.dot(v, v)
    b = np.dot(r, v)
    d = 2*particle_radius
    
    inner_term = b*b - v2*(r2 - d*d)
    if inner_term<0:
        t = 'inf'
    else:
        # The following formula has been taken from Eq: 14.2.2 in
        # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
        t = (-b - math.sqrt(inner_term))/(v2+eps)
        t = infIfNegative(t) # The collision ocurred in the past

    part_i = np.array([i])
    part_j = np.array([j])
    dt = np.array([t]) 
    times_pp = np.stack((part_i, part_j, dt), axis=1)
    return times_pp
    
def detectWallCollisionTime(i):
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

    t_left = nanIfNegative((particle_radius + x_leftWall - x)/(vx+eps))
    t_right = nanIfNegative((-particle_radius + x_rightWall - x)/(vx+eps))
    t_top = nanIfNegative((-particle_radius + y_topWall - y)/(vy+eps))
    t_bottom = nanIfNegative((particle_radius + y_bottomWall - y)/(vy+eps))
    
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

def wallCollision(i, wall):
    global vel
    i = int(i)
    wall = str(wall)

    if (wall=='left' or wall=='right'):
        vel[i,0] = -restitution_coef * vel[i,0] # x component changes direction
    elif (wall=='top' or wall=='bottom'):
        vel[i,1] = -restitution_coef * vel[i,1] # y component changes direction

def particleCollision(i, j):
    global vel
    i = int(i)
    j = int(j)
    
    r = distance(i, j)
    v = relativeVelocity(i, j)
    b = np.dot(r, v)
    # The following formula has been taken from Eq: 14.2.4 in
    # 'The Art of Molecular Dynamics Simulations', D. Rapaport.
    delta_v = (-b/(4*particle_radius*particle_radius))*r
    # TODO: a mass parameter would be useful whe expanding functionality
    vel[i] = vel[i] + delta_v 
    vel[j] = vel[j] - delta_v
    
def createWallCollisionList():
    """ Creates an ordered list times_pw with collision times 
        for all particle-wall events """
    global times_pw
    for a in range(n_particles):
        times_pw[a] = detectWallCollisionTime(a)
    times_pw = times_pw[np.array([float(a) for a in times_pw[:,2]]).argsort()]

def createCollisionList():
    """ Creates an ordered list times_pw with collision times 
        for all particle-particle events """
    global times_pp
    a = 0
    for i in range(n_particles):
        for j in range(i, (n_particles-1)):
            times_pp[a] = detectCollisionTime(i, j+1)
            a = a+1
    # TODO: When ordering i, j are presented in scientific notation ¿why?       
    times_pp = times_pp[times_pp[:,2].argsort()] 
    #times_pp[:,0] = np.array([str(int(a)) for a in times_pp[:,0]])
    #times_pp[:,1] = np.array([str(int(a)) for a in times_pp[:,1]])
            
def updateCollisionLists(t, i, j='none'):
    """ Deletes and recalculates all entries involving particles that 
        interacted in last collision """
    global times_pp, times_pw
    i = int(i)
    
    if j=='none':
        # Particle-Wall collision, recalculates only entries involving part. i
        # Delete certain entries, solution inspired by:
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-91.php
        times_pp = times_pp[~np.isin(times_pp, [i]).any(axis=1)] ################################ por aqui quiza esta el problema, refactorizar para usar listas
        times_pw = times_pw[~np.isin(times_pw, [str(i)]).any(axis=1)]
    
        # Need float conversion due to formating issues with times_pw
        times_pw_float = np.array([float(a) for a in times_pw[:,2]])
        # Now we calculate new elements and insert them in an ordered manner
        for a in range(n_particles):
            if (a==i and a!=(n_particles-1)): # Avoid i-i case
                a=a+1
            new_entry = detectCollisionTime(i, a)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        
        # Wall update
        new_entry = detectWallCollisionTime(i)
        index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        times_pw = np.insert(times_pw, index, new_entry, axis=0)
    else:
        j = int(j)
        # Particle-particle collision, recalculates entries involving i and j.
        times_pp = times_pp[~np.isin(times_pp, [i, j]).any(axis=1)]
        times_pw = times_pw[~np.isin(times_pw, [str(i), str(j)]).any(axis=1)]
        
        for a in range(n_particles):
            if (a==i and a!=(n_particles-1)): # Avoid i-i case
                a=a+1
            new_entry = detectCollisionTime(i, a)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        for a in range(n_particles):
            if ((a==j or a==i) and a!=n_particles-1): # Avoid j-j case and j-i case (already calculated)
                a=a+1
            new_entry = detectCollisionTime(j, a)
            if new_entry[0,2] == 'inf':
                index = -1
            else:
                index = bisect.bisect(times_pp[:,2], float(new_entry[0,2]))
            times_pp = np.insert(times_pp, index, new_entry, axis=0)
        
        times_pw_float = np.array([float(a) for a in times_pw[:,2]])
        
        # Wall update
        new_entry = detectWallCollisionTime(i)
        new_entry_j = detectWallCollisionTime(j)
        index = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        index_j = bisect.bisect(times_pw_float, float(new_entry[0,2]))
        times_pw = np.insert(times_pw, index, new_entry, axis=0)
        times_pw = np.insert(times_pw, index_j, new_entry_j, axis=0)
        

  
def computeNextCollision():
    """ Propagates particles until next collision and updates velocities 
        after it. Checks if next col. is particle-particle or particle-wall """
    global pos, vel
    t_pp = float(times_pp[0,2])
    t_pw = float(times_pw[0,2])
    # Check if particle-particle or particle-wall collision
    if t_pp <= t_pw:
        propagate(t_pp) # Propagate particles until current collision
        i = int(times_pp[0,0])
        j = int(times_pp[0,1])
        particleCollision(i, j) # Compute change in velocities due to collision
        updateCollisionLists(t_pp, i, j)
    else:
        propagate(t_pw)
        i = int(times_pw[0,0])
        wall = times_pw[0,1]
        wallCollision(i, wall)
        updateCollisionLists(t_pw, i)

def saveData(col_number):
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

    
# Here begins the actual script
initializeRandom()
createWallCollisionList()
createCollisionList()
for d in range(n_collisions):
    computeNextCollision()
    saveData(d)
    print("Saving file for colission nº: " + str(d))