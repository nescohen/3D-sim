import numpy as np
import numpy.typing as npt

def new_vector(x: float, y: float, z: float) -> npt.NDArray:
	return np.array([[x], [y], [z]])

def upwards_component(obj: dict) -> float:
    gz = new_vector(0, 0, 1)
    lz = obj["orientation"].dot(gz)
    return np.transpose(gz).dot(lz) / (np.linalg.norm(gz) * np.linalg.norm(lz))

arm1 = new_vector(1, 1, 0)
arm2 = new_vector(1, -1, 0)
arm3 = new_vector(-1, 1, 0)
arm4 = new_vector(-1, -1, 0)

arms = [arm1, arm2, arm3, arm4]

power = 4

def control(obj: dict, dt: float) -> list[float]:
    gravity = 9.81*obj["mass"]
    print(upwards_component(obj))
    control = gravity / 4 / power / upwards_component(obj)
    return [control, control, control, control]
