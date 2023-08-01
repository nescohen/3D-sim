import numpy as np

def new_physics_object(pos, orientation, vel, acc, mass):
    return {
        "position": pos, #vector
        "orientation": orientation, #matrix
        "velocity":vel, #vector
		"acceleration": acc, #vector
        "mass": mass, #scalar
        "force": new_vector(0,0,0) #vector
    }

def apply_force(physics_object, F):
    physics_object["acceleration"] = physics_object["acceleration"] + (F / physics_object["mass"])
    
def update_physics(physics_object, dt):
    
    physics_object["acceleration"] =  physics_object["acceleration"] + physics_object["force"] / physics_object["mass"]
    physics_object["velocity"] = physics_object["velocity"] + (physics_object["acceleration"] * dt)
    physics_object["position"] = physics_object["position"] + (physics_object["velocity"] * dt)
    