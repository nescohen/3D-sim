
# Supports Python Modules: builtins, math,pandas, scipy 
# matplotlib.pyplot, numpy, operator, processing, pygal, random, 
# re, string, time, turtle, urllib.request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time
import random

def rotation_matrix(radians):
  return np.matrix([
    [np.cos(radians), -1*np.sin(radians)], 
    [np.sin(radians), np.cos(radians)]
    ])

joint_coefficients = [random.uniform(-1, 1) for c in range(4)]
print(joint_coefficients)

def joint_angles(timestep):
  return [timestep*c for c in joint_coefficients]

def joints_time(timestep):
  angles = joint_angles(timestep)
  return list(map(lambda t: rotation_matrix(t), angles))

links = [np.mat('1; 0'), np.mat('1; 0'), np.mat('1; 0'), np.mat('1; 0')]
start = np.matrix('0; 0')

def draw_arm(start, links, joints):
  rot = np.identity(2)
  pos = start
  result_rot = []
  result_pos = [start]
  for index, link in enumerate(links):
    rot = rot * joints[index]
    result_rot.append(rot)
    rotated = rot * link
    pos = pos + rotated
    result_pos.append(pos)
  return result_pos


plt.style.use('_mpl-gallery')
plt.ion()

# plot
fig, ax = plt.subplots()
  
ax.set(xlim=(-4, 4), ylim=(-4, 4))

line, = ax.plot([], [], linewidth=2.0)

def refresh_plot(xd, yd):
  line.set_xdata(xd)
  line.set_ydata(yd)
  fig.canvas.draw()
  fig.canvas.flush_events()
         
plt.show() 

timestep = 0
while True:
  timestep += 0.05
  joints_array = joints_time(timestep)
  rendered = draw_arm(start, links, joints_array)
  x = list(map(lambda point: point.item(0), rendered))
  y = list(map(lambda point: point.item(1), rendered))
  refresh_plot(x, y)
  time.sleep(0.05)