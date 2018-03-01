"""
Created on Thu Feb 15 12:23:03 2018

@author: Miguel Ángel López Castaño
"""
#TODO: Comentar mas todo el proceso ----------------------------------------------------------
from initialization import initRandomPos, initRandomVel
from tools import saveData
from timeLists import createCollisionList, createWallCollisionList
from mainLoop import computeNextCollision
from tools import deleteInfs

#eps = 5000*np.finfo(float).eps # Machine epsilon

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
restitution_coef = 1.0
particle_radius = 1.0
n_particles = 5 #por que minimo 3?
desired_collisions_per_particle = 10
n_collisions = n_particles*desired_collisions_per_particle

scale_factor = 20
form_factor = 16/9

size_X = scale_factor*particle_radius
size_Y = scale_factor*particle_radius/form_factor
        
##################################################################################### unificar listas de tiempo en una sola

# Here begins the actual script
pos = initRandomPos(particle_radius, n_particles, size_X, size_Y)
vel = initRandomVel(n_particles)
times_pw = createWallCollisionList(n_particles, particle_radius, size_X, size_Y, pos, vel)
times_pp = createCollisionList(n_particles, particle_radius, pos, vel)

times_pp = deleteInfs(times_pp)

# We call the main loop for every collision
for c in range(n_collisions):
    result = computeNextCollision(n_particles, particle_radius, size_X, size_Y, 
                                  restitution_coef, pos, vel, times_pp, times_pw)
    pos = result[0]
    vel = result[1]
    times_pp = result[2]
    times_pw = result[3]
    print(times_pp)
    print(times_pw)
    
    saveData(c, data_folder, n_particles, pos, vel)
    print("Saving file for colission nº: "+str(c+1)+" / "+str(n_collisions))

print("Simulation finished, data can be found in: " + data_folder)