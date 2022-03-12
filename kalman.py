import numpy as np


class Kalman:
    def __init__(self, param: list):
        self.A = param['A']
        self.dim = self.A.shape[0]
        self.B = param['B']
        self.C = param['C']
        self.R = param['control_cov']
        self.Q = param['noise_cov']
        self.Sigma = np.diag(np.zeros(self.dim))

    def filter(self, mu: list, u: list, z: list) -> list:
        """
        run the kalman filter for one loop
        :param mu: current state
        :param u: control input
        :param z: observation input
        :return next state
        """
        # prediction
        mu_new = self.A @ mu + self.B @ u
        Sigma_new = self.A @ self.Sigma @ self.A.T + self.R
        # correction
        K = Sigma_new @ self.C.T @ np.linalg.inv(
            self.C @ Sigma_new @ self.C.T + self.Q)
        mu_new = mu_new + K @ (z - self.C @ mu_new)
        Sigma_new = (np.eye(self.dim) - K @ self.C) @ Sigma_new
        self.Sigma = Sigma_new
        return mu_new
