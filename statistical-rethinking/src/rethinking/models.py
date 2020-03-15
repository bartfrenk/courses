import numpy as np


def polynomial_design_matrix(xs, n):
    return np.repeat([xs], n, axis=0).transpose() ** range(1, n + 1)
