# -*- coding: utf-8 -*-
"""
Created on Mon May 28 19:25:21 2018

@author: malopez
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_folder = "C:/Users/malopez/Desktop/disksMD/data"
output_image = './plot.png'
alphas = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]


size_X_inches = 8
size_Y_inches = 6
size_figure = (size_X_inches, size_Y_inches)

fig, ax = plt.subplots(figsize=size_figure, dpi=250)
ax.set_xlim([0,1])

a2s = []

for alpha in alphas:
    file_name = data_folder + "/a2_alpha"+str(alpha)+".dat"
    data = pd.read_table(file_name, sep='\s+', 
                         header = None, names =['x', 'y'])
    # Promediar ultimas 1500 colisiones
    mean_a2 = data.iloc[-2000:,1].mean()
    a2s.append(mean_a2)

plt.scatter(alphas, a2s, marker='o')
# Fit
plt.plot(np.unique(alphas), np.poly1d(np.polyfit(alphas, a2s, 10))(np.unique(alphas)))
plt.axhline(y=0.0, color='black', linestyle='-')
plt.show()
fig.savefig(output_image)
plt.close()