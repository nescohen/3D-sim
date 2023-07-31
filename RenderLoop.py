import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time

def new_vector(x, y, z):
    return np.matrix([
        [x],
        [y],
        [z]
    ])

def matrix_from_set(vector_set):
    vector_matrix = np.zeros(3, vector_set.Len())
    for i in range(0, vector_set.Len()-1):
        for n in range(0,2):
            vector_matrix.itemset((n, i), vector_set[i].item(n))
    return vector_matrix
    
def set_from_matrix(matrix):
    vector_set = list()
    for i in range(0, (matrix.shape[1] - 1)):   
        vector_set.append(new_vector(matrix.item((0,i)), matrix.item((1,i)), matrix.item((2,i))))
    return vector_set
    
def rotate_matrix(matrix, rotation_matrix):
    return rotation_matrix * matrix   
    
def rotation_matrix_x(radians):
    return np.matrix([
        [1 , 0 , 0],
        [0 , np.cos(radians), -1*np.sin(radians)], 
        [0, np.sin(radians), np.cos(radians)]
        ])
        
def rotation_matrix_y(radians):
    return np.matrix([
        [np.cos(radians), 0 , np.sin(radians)],
        [0 , 1 , 0],
        [-1*np.sin(radians), 0 , np.cos(radians)]
        ])
        
def rotation_matrix_z(radians):
    return np.matrix([
        [np.cos(radians), -1*np.sin(radians), 0],
        [np.sin(radians) , np.cos(radians), 0],
        [0 , 0 , 1]
        ])
        
def rotation_matrix(axis, radians):
    if axis == 'x':
        return rotation_matrix_x(radians)
    if axis == 'y':
        return rotation_matrix_y(radians)
    if axis == 'z':
        return rotation_matrix_z(radians)
        
def new_plot(fig_num):
    fig = plt.figure(fig_num)
    return fig
    
# def new_axis(x_lim, y_lim, z_lim):
#     ax = plt.axes(projection='3d')
#     if x_lim.type() == list:
#         ax.set(xlim = x_lim, ylim = y_lim, zlim = z_lim)
#     if x_lim.type() == int:
#         ax.set(xlim = [x_lim, -1*x_lim], ylim = [y_lim, -1*y_lim], zlim = [z_lim, -1*z_lim])
#     else:
#         ax.set(xlim = [1, -1], ylim = [1, -1], zlim = [1, -1])
#     return ax
    
def new_line(axis, start, end):
    data = list()
    for i in range(0,2):
        data[i] = [start(i), end(i)]
    line = axis.Plot3D(data[0], data[1], data[2], linewidth=2.0)
    return line
    
def update_plot(fig):
    fig.canvas.draw()
    fig.canvas.flush_events()

# Main   
Plot = new_plot(1)
# Axis = new_axis([-3,3], [-3,3], [-3,3])
v_set = new_vector_set(2)

while True:
    update_plot(Plot)
    time.sleep(0.05)