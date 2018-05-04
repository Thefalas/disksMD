# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:33:28 2018

@author: malopez
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

images_folder = "C:/Users/malopez/Desktop/disksMD/images"
data_folder = "C:/Users/malopez/Desktop/disksMD/data"
particle_radius = 1.0
n_particles = 50 # TODO: Why 3 is the minimun number of particles?
desired_collisions_per_particle = 10
n_collisions = n_particles*desired_collisions_per_particle
size_X = 30 # System size X
size_Y = 30 # System size Y


for i in range(n_collisions):
    file_name_pos = data_folder + "/xy"+'{0:04d}'.format(i)+".dat"
    pos = pd.read_table(file_name_pos, sep='\s+', 
                        header = None, names =['x', 'y'])
    
    img_name = images_folder+'/img'+'{0:04d}'.format(i)+".png"
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    ax.set_xlim([0,30])
    ax.set_ylim([0,30])
    plt.scatter(pos.x, pos.y, s=475)
    fig.savefig(img_name)
    print('Saving img nº: '+str(i))
    plt.close()
  
images = []
output = './video.mp4'
for i in range(n_collisions):
    images.append(images_folder+'/img'+'{0:04d}'.format(i)+".png")

# Height and Width from first image
frame = cv2.imread(images[0])
height, width, channels = frame.shape

# Definimos el codec y creamos un objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out = cv2.VideoWriter(output, fourcc, 30.0, (width, height))

for image in images:

    frame = cv2.imread(image)

    out.write(frame) # Write out frame to video

# Release everything if job is finished
out.release()

print("The output video is {}".format(output))