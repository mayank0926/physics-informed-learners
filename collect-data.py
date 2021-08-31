import gym
import mujoco_py
import numpy as np
from numpy.lib.function_base import append
import scipy.io as sc

obj_init = np.array([1, 1, 0.42, 1, 1, 0], dtype=np.float32)
# [initial object coordinates, initial object velocity]

env = gym.make('mujoco_collection_1:mujoco-slide-v0', obj_init=obj_init)
env.reset()
done = False
obs = None
iter = 0
data = np.array([[0,0,0,1.5,0.75]])
print(np.shape(data))
while not done:
  # if iter>18000:
  #   env.render(mode="human")
  obs, reward, done, info = env.step(env.action_space.sample())
  displacement = obs["obj_pos"][:2] - obj_init[:2]
  seethis = obs["obj_vel"]
  x = displacement[0]
  y= displacement[1]
  x_dot = seethis[0]
  y_dot = seethis[1]
  
  newrow = np.array([[0.04*(iter+1), x, y, x_dot, y_dot]])
  data = np.vstack([data, newrow])
  iter += 1
  # if(done and iter>100):
  #   break
np.savetxt("data1.csv", data, delimiter=",")
sc.savemat("data1.mat", {'data':data})
print(np.shape(data))
displacement = obs["obj_pos"][:2] - obj_init[:2]
final_velocity = obs["obj_vel"]
print(f"Completed in {iter} steps, displacement = {displacement}, velocity = {final_velocity}")
env.close()