import numpy as np
import scipy.stats
from scipy.stats.stats import _euclidean_dist
from noise import gaussian_noise
from math import inf, sqrt
from config import *

from utils import draw_sphere_marker


class Particle:
    def __init__(self, param: list):
        self.sample_times = param['particle_sample_times']
        self.A = param['A']
        self.state_dim = self.A.shape[0]
        self.B = param['B']
        self.C = param['C']
        self.R = param['control_cov']
        self.Q = param['noise_cov']
        self.sample_cov = param['particle_sample_cov']
        self.particles: list = []
        for _ in range(self.sample_times):
            self.particles.append(gaussian_noise((0, 0, 0), self.sample_cov))

    def filter(self,u: list, z: list) -> list:
        """
        run the particle filter for one loop
        :param u: control input
        :param z: observation input
        :return next state
        """
        samples: list = []
        # update
        for particle in self.particles:
            # predict new particle location using control covariance
            new_particle = gaussian_noise(self.A @ particle + self.B @ u,
                                          self.R)
            weight = self.euclidean_weight(new_particle, z)
            samples.append([new_particle, weight])

        # process weight in ordered form
        sum = 0
        for sample in samples:
            sum += sample[1]
            sample[1] = sum


        # resample
        self.particles.clear()
        #method 1
        for _ in range(self.sample_times):
            rand_num = np.random.rand() * sum
            # binary search
            left = 0
            right = len(samples)
            while left != right:
                candidate = left + int((right - left) / 2)
                if samples[candidate][1] >= rand_num: right = candidate
                else: left = candidate + 1
            # sample candidate
            self.particles.append(samples[left][0])
        #method 2
        # for sample in samples:
        #     sample[1] = sample[1]/sum
        # r = np.random.rand() / self.sample_times
        # index = 0
        # for _ in range(self.sample_times):
        #     while samples[index][1] < r: index += 1
        #     # sample candidate
        #     self.particles.append(samples[index][0])
        #     r += 1/self.sample_times


        # return mean of particles
        mean = np.mean(self.particles, axis=0)
        if DEBUG:
            var = np.var(self.particles, axis=0)
            print("Particle var: ", var)
        # self.draw_particles()
        return mean

    def euclidean_weight(self, v: list, z: list) -> float:
        """
        :param v: state vector
        :param z: esimation vector
        :return weight of state v given estimation z
        """
        assert (len(v) == len(z))
        err = 0
        sum = 0
        for i in range(2):
            sum += (v[i] - z[i])**2
        if sum < err: return 1 / err
        return 1 / sum

    def draw_particles(self) -> None:
        for particle in self.particles:
            draw_sphere_marker((particle[0], particle[1], 1), 0.1,
                               (1, 1, 0, 1))
