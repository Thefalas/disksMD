# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:33:28 2018

@author: malopez
"""
import pandas as pd
import matplotlib.pyplot as plt
import cv2

images_folder = "C:/Users/malopez/Desktop/disksMD/images"
data_folder = "C:/Users/malopez/Desktop/disksMD/data"
output_video = './video4.mp4'
particle_radius = 1.0
n_particles = 90 # TODO: Why 3 is the minimun number of particles?
desired_collisions_per_particle = 10
n_collisions = n_particles*desired_collisions_per_particle
size_X = 60 # System size X
size_Y = 30 # System size Y

size_X_inches = 6*(size_X/size_Y)
size_Y_inches = 6
size_figure = (size_X_inches, size_Y_inches)
# Fenomenological constant ;p
circle_size = 11875*size_X_inches*size_Y_inches / (size_X*size_Y)
# circle_size = particle_radius*427500 / (size_X*size_Y)


for i in range(n_collisions):
    file_name_pos = data_folder + "/xy"+'{0:05d}'.format(i)+".dat"
    pos = pd.read_table(file_name_pos, sep='\s+', 
                        header = None, names =['x', 'y'])
    
    img_name = images_folder+'/img'+'{0:05d}'.format(i)+".png"
    fig, ax = plt.subplots(figsize=size_figure, dpi=250)
    ax.set_xlim([0,size_X])
    ax.set_ylim([0,size_Y])
    plt.scatter(pos.x, pos.y, s=circle_size)
    fig.savefig(img_name)
    print('Saving img nº: '+str(i))
    plt.close()
  
images = []

for i in range(n_collisions):
    images.append(images_folder+'/img'+'{0:05d}'.format(i)+".png")

# Height and Width from first image
frame = cv2.imread(images[0])
height, width, channels = frame.shape

# Definimos el codec y creamos un objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out = cv2.VideoWriter(output_video, fourcc, 30.0, (width, height))

print('Generating video, please wait')
for image in images:

    frame = cv2.imread(image)
    # Write out frame to video
    out.write(frame) 

# Release everything if job is finished
out.release()

print("The output video is {}".format(output_video))