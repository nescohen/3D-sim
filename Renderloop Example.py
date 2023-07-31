import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time

#MATH STUFF
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

def create_vector(x, y, z):
    return np.matrix([
        [x],
        [y],
        [z]
    ])
    
def rotated_vector(v, rotation_matrix):
    return rotation_matrix * v
    
    
    
fig = plt.figure()

ax = plt.axes(projection='3d')

ax.set(xlim=(-3, 3), ylim=(-3, 3), zlim =(-3, 3))

line1, = ax.plot3D([], [], [], linewidth=2.0)
line2, = ax.plot3D([], [], [], linewidth=2.0)
line3, = ax.plot3D([], [], [], linewidth=2.0)
plt.style.use('_mpl-gallery')
plt.ion()
plt.show()

def object_state(position_vector, rotation_matrix):

    rotated_x_vector = rotated_vector(create_vector(1,0,0) , rotation_matrix) 
    rotated_y_vector = rotated_vector(create_vector(0,1,0) , rotation_matrix)
    rotated_z_vector = rotated_vector(create_vector(0,0,1) , rotation_matrix)
    
    trans_vect_x = rotated_x_vector + position_vector
    trans_vect_y = rotated_y_vector + position_vector
    trans_vect_z = rotated_z_vector + position_vector
    
    line1.set_data_3d(
    [position_vector.item(0), trans_vect_x.item(0)],
    [position_vector.item(1), trans_vect_x.item(1)],
    [position_vector.item(2), trans_vect_x.item(2)]
    )
    
    line2.set_data_3d(
    [position_vector.item(0), trans_vect_y.item(0)],
    [position_vector.item(1), trans_vect_y.item(1)],
    [position_vector.item(2), trans_vect_y.item(2)]
    )
    line3.set_data_3d(
    [position_vector.item(0), trans_vect_z.item(0)],
    [position_vector.item(1), trans_vect_z.item(1)],
    [position_vector.item(2), trans_vect_z.item(2)]
    )
#SCREEN STUFF

def refresh_plot(timestep, rotation_matrix):
    object_state(create_vector(timestep,timestep,timestep), rotation_matrix) 
    fig.canvas.draw()
    fig.canvas.flush_events()
  
timestep = 0

while True:
    timestep += 0.01
    refresh_plot(timestep, rotation_matrix('x', timestep) * rotation_matrix('y', timestep) * rotation_matrix('z', timestep))
    time.sleep(0.05)
    