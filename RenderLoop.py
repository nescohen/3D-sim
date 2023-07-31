import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time

def new_render_object(pos, orientation, lines):
    return {
        "position": pos,
        "orientation": orientation,
        "lines": lines
    }

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
    
def new_axis(x_lim, y_lim, z_lim):
    ax = plt.axes(projection='3d')
    ax.set(xlim = x_lim, ylim = y_lim, zlim = z_lim)
    return ax
    
def new_line(axis):
    line, = axis.plot3D([], [], [], linewidth=2.0)
    return line

def update_line(line, start, end):
    data = list()
    for i in range(3):
        data.append([start.item(i), end.item(i)])
    line.set_data_3d(data[0], data[1], data[2])
    
def draw_object_state(render_object):

    position_vector = render_object["position"]
    rotation_matrix = render_object["orientation"]
    lines = render_object["lines"]

    basis_vectors = [new_vector(1,0,0), new_vector(0,1,0), new_vector(0,0,1)]
    rotated_vectors = [(rotation_matrix * v) for v in basis_vectors]
    translated_vectors = [(position_vector + r) for r in rotated_vectors]
    for (l, v) in zip(lines, translated_vectors):
        update_line(l, position_vector, v)

def update_plot(fig):
    fig.canvas.draw()
    fig.canvas.flush_events()

# Main
plt.style.use('_mpl-gallery')
plt.ion()
plt.figure(figsize=(10, 8), dpi=80)
p = new_plot(1)
axis = new_axis([-3,3], [-3,3], [-3,3])
plt.show()

render_lines = [new_line(axis) for i in range(3)]

timestep = 0

while True:
    timestep += 0.05
    object_example = new_render_object(new_vector(0, 0, 0), rotation_matrix('z', timestep), render_lines)
    draw_object_state(object_example)
    update_plot(p)
    time.sleep(0.05)