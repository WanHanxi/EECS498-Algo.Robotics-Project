import numpy as np


def gen_noise(pt: np.array, param: list) -> list:
    if param['type'] == 'normal': return gaussian_noise(pt, param['cov'])
    elif param['type'] == 'uniform': return uniform_noise(pt, param['cov'])


def gaussian_noise(pt: np.array, cov: np.matrix) -> list:
    # var = np.diag(cov)
    # return np.array([np.random.normal(v, var[i]) for i, v in enumerate(pt)])
    return np.random.multivariate_normal(pt, cov, 1)[0]


def uniform_noise(pt: np.array, cov: np.matrix) -> list:
    ret = np.zeros(len(pt))
    for i in range(len(pt)):
        ret[i] = pt[i] + (np.random.rand() - 0.5) * 6 * np.diag(cov)[i]
    return ret