"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
import math
import random
import bisect
import numpy as np

restitution_coef = 1.0
particle_radius = 1.0
n_particles = 300
desired_collisions_per_particle = 8
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
    dist = pos[i] - pos[j]
    return dist

def distanceModulus(i, j):
    """ Measures the distance modulus between two particles i, j """
    dist_X = pos_X[j] - pos_X[i]
    dist_Y = pos_Y[j] - pos_Y[i]
    dist = math.sqrt(dist_X*dist_X + dist_Y*dist_Y)
    return dist

def relativeVelocity(i, j):
    """ Measures the relative velocity between two particles i, j """
    rel_v = vel[i] - vel[j]
    return rel_v

def infIfNegative(t):
    if t < 0:
        return 'inf'
    else:
        return t

def nanIfNegative(t):
    if t < 0:
        return math.nan
    else:
        return t

def propagate(t):
    """ Updates positions for all particles, lineal movement during a time t
        It also modifies the lists containig collision times to reflect the
        time that has passed """
    for i in range(n_particles):
        pos[i] = pos[i] + vel[i]*t
    for i in range(n_particles):
        times_pp[i,2] = times_pp[i,2] - t
        times_pw[i,2] = times_pw[i,2] - t
        
def detectCollisionTime(i, j):
    """ Returns the time until the next collision between particles i, j """
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
        t = (-b - math.sqrt(inner_term))/v2
        t = infIfNegative(t) # The collision ocurred in the past

    part_i = np.array([str(i)])
    part_j = np.array([str(j)])
    dt = np.array([t]) 
    times_pp = np.stack((part_i, part_j, dt), axis=1)
    return times_pp
    
def detectWallCollisionTime(i):
    """ Returns the time until particle i hits a wall """
    x = pos[i, 0]
    y = pos[i, 1]
    vx = vel[i, 0]
    vy = vel[i, 1]
    
    x_leftWall = 0.0
    x_rightWall = size_X
    y_topWall = size_Y
    y_bottomWall = 0.0

    t_left = (particle_radius + x_leftWall - x)/vx
    t_right = (-particle_radius + x_rightWall - x)/vx
    t_top = (-particle_radius + y_topWall - y)/vy
    t_bottom = (particle_radius + y_bottomWall - y)/vy
    
    part_i = np.array([i for a in range(4)])
    dt = np.array([t_left, t_right, t_top, t_bottom])
    wall = np.array(['left', 'right', 'top', 'bottom'])
    
    times_pw = np.stack((part_i, wall, dt), axis=1)
    times_pw[:,2] = [nanIfNegative(float(a)) for a in times_pw[:,2]]
    # We need to sort the list in order to return only the element 
    # with the lowest collision time. This approach is similar to the
    # one found at: https://stackoverflow.com/a/2828121
    # More complex cause float conversion is needed for times column in array.
    times_pw = times_pw[np.array([float(a) for a in times_pw[:,2]]).argsort()]
    return times_pw[0]

def wallCollision(i):
    wall = times_pw[i,1] # Determine wich wall the particle has collided with
    if (wall=='left' or wall=='right'):
        vel[i,0] = -restitution_coef * vel[i,0] # x component changes direction
        vel[i,1] = restitution_coef * vel[i,1]
    elif (wall=='top' or wall=='bottom'):
        vel[i,1] = -restitution_coef * vel[i,1] # y component changes direction
        vel[i,0] = restitution_coef * vel[i,0]

def particleCollision(i, j):
    vel[i] = vel[i] #Operaciones necesarias, habria que añadir un parámetro masa
    vel[j] = vel[j]

def collision (i, j='none'):
    """ Computes the change in velocities after a collision between i, j """
    if j=='none':
        wallCollision(i)
    else:
        particleCollision(i, j)
    
def updateTimeLists(i, j='none'):
    """ Deletes all registries involving particles i, j and recalculates
        collision times involving those particles, j as an optional param. """
    if j=='none':
        # Recalcula solo las colisiones relacionadas con i
        times_pw[i] = detectWallCollisionTime(i)
        #times_pp =
    else:
        # Recalcula las colisiones relacionadas con i, j
        times_pw[i] = detectWallCollisionTime(i)
        times_pw[j] = detectWallCollisionTime(j)

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
            
def updatecollisionLists():
    return 0
    
# Here begins the actual script
initializeRandom()
createWallCollisionList()
createCollisionList()
print(times_pw)
print(times_pp)
        #bisect.bisect(np.array([float(a) for a in prueba[:,2]]))
        #bisect.insort(prueba, tau) # Bisect for creating an ordered list

# Crear dos listas / diccionarios, colisiones entre particulas y colisiones con pared
# Coger el primer elemento de ambas y ver cual es mas pequeño
#bisect.insort( listacolmuro, [vdt,[i,im]] )
#bisect.insort( listacol, [vdt,[i,j]] )