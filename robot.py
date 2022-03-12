import numpy as np
import math
from utils import get_angle


class Robot:
    def __init__(self, control_cov):
        self.pose_ground_truth = np.array([0, 0, 0])
        self.pose_sensor = np.array([0, 0, 0])
        self.pose_estimated = np.array([0, 0, 0])
        self.pose_estimated1 = np.array([0, 0, 0])
        self.control_cov = control_cov

    def update(self, control):
        old_pose = self.pose_ground_truth
        self.pose_ground_truth = self.pose_ground_truth  + control \
        + np.random.multivariate_normal( [0, 0, 0], self.control_cov, 1)[0]
        self.pose_ground_truth[2] = get_angle(old_pose, self.pose_ground_truth)
