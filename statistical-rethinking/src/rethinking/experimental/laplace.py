import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression


def _compute_location(f, x_):
    # This does not always find the mode
    maximum = minimize(lambda x: -f(x), x_, method="BFGS")
    maximum.fun = -maximum.fun
    return maximum.x[0]


def _compute_scale(f, x0, dx=0.1, k=5):
    g = lambda x: np.log(f(x)) - x0
    xs = np.linspace(x0 - dx, x0 + dx)
    ys = np.array([g(x) for x in xs])
    arrays = []
    for n in range(1, k + 1):
        t = xs ** n
        t = t.reshape((len(t), 1))
        arrays.append(t)
    phi = np.hstack(arrays)
    res = LinearRegression().fit(phi, ys)
    return np.sqrt(-1 / (2 * res.coef_[1]))


def laplace_approximation(f, x_, dx=0.1):
    location = _compute_location(f, x_)
    scale = _compute_scale(f, location, dx)
    return (location, scale)
