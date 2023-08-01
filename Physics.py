import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import time
import typing
import numpy.typing as npt
import math

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
		force: typing.Callable[[dict], npt.NDArray],
	) -> dict:
	return {
		"mass": mass,
		"radius": radius,
		"position": position,
		"orientation": orientation,
		"linear_velocity": lin_vel,
		"angular_velocity": ang_vel,
		"drag_coefficient": drag_co,
		"force": force,
	}

def new_state(obs: list[dict]) -> dict:
	return {
		"time": float(0),
		"objects": obs
	}


def object_step(obj: dict) -> dict:
	new_object = {**obj}
	force = obj["force"](obj)
	acceleration = force / obj["mass"]
	new_object["linear_velocity"] = obj["linear_velocity"] + acceleration * TIMESTEP_S
	new_object["position"] = obj["position"] + new_object["linear_velocity"] * TIMESTEP_S
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

def environment_model(obj: dict) -> npt.NDArray:
	gravity = new_vector(0, 0, -9.81*obj["mass"])

	speed = np.linalg.norm(obj["linear_velocity"])
	air_density = 1.2
	area = np.pi * obj["radius"]**2

	v2 = obj["linear_velocity"] * speed
	air_resistance = -0.5 * air_density * area * obj["drag_coefficient"] * v2

	return gravity + air_resistance