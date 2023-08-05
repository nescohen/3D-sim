import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time
import typing
import numpy.typing as npt
import math
import functools
import RenderLoop as render
import Control as control

TIMESTEP_S: float = 0.01

def new_vector(x: float, y: float, z: float) -> npt.NDArray:
	return np.array([[x], [y], [z]])

def new_object(
		mass: float,
		radius: float,
		position: npt.NDArray,
		orientation: npt.NDArray,
		lin_vel: npt.NDArray,
		ang_vel: npt.NDArray,
		drag_co: float,
		local_forces,
		global_forces,
	) -> dict:
	return {
		"mass": mass,
		"radius": radius,
		"position": position,
		"orientation": orientation,
		"linear_velocity": lin_vel,
		"angular_velocity": ang_vel,
		"drag_coefficient": drag_co,
		"local_forces": local_forces,
		"global_forces": global_forces,
	}

def new_state(obs: list[dict]) -> dict:
	return {
		"time": float(0),
		"objects": obs
	}

def cross(a, b):
	return np.transpose(np.cross(np.transpose(a), np.transpose(b)))

def object_step(obj: dict) -> dict:
	new_object = {**obj}
	local_forces = obj["local_forces"](obj)
	global_forces = obj["global_forces"](obj)
	net_force = new_vector(0, 0, 0)
	net_torque = new_vector(0, 0, 0)
	for (f, a) in local_forces:
		net_force = net_force + obj["orientation"].dot(f)
		net_torque = net_torque + cross(f, a)
	for (f, a) in global_forces:
		net_force = net_force + f
		net_torque = net_torque + cross(np.linalg.inv(obj["orientation"]).dot(f), a)
	acceleration = net_force / obj["mass"]
	new_object["linear_velocity"] = obj["linear_velocity"] + acceleration * TIMESTEP_S
	new_object["position"] = obj["position"] + new_object["linear_velocity"] * TIMESTEP_S
	moi = 2.0 / 5.0 * obj["mass"] * obj["radius"]**2 # Assuming all objects are spheres with uniform density
	angular_acc = net_torque / moi
	new_object["angular_velocity"] = obj["angular_velocity"] + angular_acc * TIMESTEP_S
	new_object["orientation"] = obj["orientation"] * render.rotation_matrix(new_object["angular_velocity"], TIMESTEP_S * np.linalg.norm(new_object["angular_velocity"]))
	return new_object

def sim_step(state: dict) -> dict:
	new_objects = [object_step(obj) for obj in state["objects"]]
	new_state = {
		**state,
		"time": state["time"] + TIMESTEP_S,
		"objects": new_objects
	}
	return new_state

def sim_run(start_state: dict, steps: int) -> dict:
	curr_state = start_state
	for _ in range(steps):
		curr_state = sim_step(curr_state)
	return curr_state

def global_force_model(obj: dict) -> list[(npt.NDArray, npt.NDArray)]:
	com = new_vector(0, 0, 0)

	gravity = new_vector(0, 0, -9.81*obj["mass"])

	speed = np.linalg.norm(obj["linear_velocity"])
	air_density = 1.2
	area = np.pi * obj["radius"]**2

	v2 = obj["linear_velocity"] * speed
	air_resistance = -0.5 * air_density * area * obj["drag_coefficient"] * v2

	return [
		(gravity, com),
		(air_resistance, com),
	]
 

## Forces are returned in the object's local frame
def local_force_model(obj: dict) -> list[(npt.NDArray, npt.NDArray)]:
	com = new_vector(0, 0, 0)

	controls = control.control(obj, TIMESTEP_S)
	motor = new_vector(0, 0, 4) # newtons

	arm1 = new_vector(1, 1, 0)
	arm2 = new_vector(1, -1, 0)
	arm3 = new_vector(-1, 1, 0)
	arm4 = new_vector(-1, -1, 0)

	arms = [arm1, arm2, arm3, arm4]
	forces = [(motor * c, a) for (c, a) in zip(controls, arms)]
	print(forces)

	return forces