import numpy as np
from numpy.core.fromnumeric import reshape, shape
from numpy.lib.function_base import append
import scipy.io as sc
import time
from tqdm import tqdm

def toy_datagen(config):
	# Final shape of collected data is (config['TOTAL_ITERATIONS'], V_VALUES)
	# collected_data = np.zeros(shape=(len(config['t_range']),1), dtype=np.float32)
	collected_data = np.array(config['t_range']).reshape((len(config['t_range']),1))

	for vx in tqdm(config['vx_range'], desc = 'Toy data generation progress'):
		data = np.zeros((len(config['t_range']),1), dtype=np.float32)
		stopping_time = vx/(-1*config['acc'])
		stopping_distance = (vx**2)/(-2*config['acc'])

		for t in range(len(config['t_range'])):
			if (config['t_range'][t]>=stopping_time):
				data[t][0] = (stopping_distance)
			else:
				data[t][0] = (vx*config['t_range'][t] + 0.5*config['acc']*(config['t_range'][t]**2))

		collected_data = np.hstack([collected_data, data])

	collected_data = np.vstack([np.zeros(shape=(1,1+len(config['vx_range']))), collected_data])
	collected_data[0, 0] = -np.inf
	collected_data[0, 1:] = config['vx_range']

	if config['save_collected']:
		np.savetxt(config['datadir'] + config['datafile'], collected_data, delimiter=",")

if __name__=="__main__":
  print("Please call this from collection constants file.")