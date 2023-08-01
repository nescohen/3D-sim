import matplotlib.pyplot as plt
import Physics as phy
import RenderLoop as render
import time
import numpy as np

def draw_physics_object(lines, obj: dict) -> dict:
    return render.new_render_object(obj["position"], obj["orientation"], lines)

plt.style.use('_mpl-gallery')
plt.ion()
plt.figure(figsize=(10, 8), dpi=80)
p = render.new_plot(1)
axis = render.new_axis([-3,3], [-3,3], [-3,3])
plt.show()

render_lines = [render.new_line(axis) for i in range(3)]

timestep = 0

state = phy.new_state([phy.new_object(100, 1, phy.new_vector(0, 0, 0), np.identity(3), phy.new_vector(0, 0, 0), phy.new_vector(0, 0, 0), 0.47, phy.environment_model)])

while True:
    timestep += 0.01
    state = phy.sim_run(state, 1)
    ro = draw_physics_object(render_lines, state["objects"][0])
    render.draw_object_state(ro)
    render.update_plot(p)
    time.sleep(0.01)