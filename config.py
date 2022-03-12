import numpy as np
from enum import Enum
#### {{ PATH
# circle path
# path_param = {'type': 'circle', 'radius': 10, 'step': 0.1}

# L-turn
# path_param = {'type': 'L-turn', 'step': 0.1}

# eecs
path_param = {'type': 'eecs', 'step': 0.3}
#### }}

#### {{ Simulation
noise_param = {'type': 'normal', 'cov': np.diag([0.3, 0.3, 0.1])}
ground_truth_control_cov = np.diag([0.02,0.02,0.01])
RENDER_GUI = True
DEBUG = False
PLOT = True
PLOT_LINE_WIDTH = 5
#### }}


####{{ Filter
class FilterType(Enum):
    Kalman = 0
    Particle = 1
    Both = 2


# FILTER: FilterType = FilterType.Kalman
filter_param = {
    'A': np.eye(3),
    'B': np.eye(3),
    'C': np.eye(3),
    'noise_cov': np.diag([1, 1, 0.05]),
    'control_cov': np.diag([0.1,0.1,0.01]),
    'particle_sample_times': 300,
    'particle_sample_cov': np.diag([0.1, 0.1, 0.1])  # covariance of sampling
}
#### }}