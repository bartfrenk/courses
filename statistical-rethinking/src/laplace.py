from scipy.optimize import minimize_scalar
from scipy.stats import norm
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def compute_location(f):
    maximum = minimize_scalar(lambda x: -f(x))
    maximum.fun = -maximum.fun
    return maximum.x


def compute_scale(f, x, dx=0.1):
    g = lambda x: np.log(f(x)) - x
    xs = np.linspace(x - dx, x + dx)
    ys = np.array([g(x) for x in xs])
    phi = xs ** 2
    phi = phi.reshape((len(phi), 1))
    res = LinearRegression().fit(phi, ys)
    return -res.coef_[0]


def main():
    f = norm.pdf
    location = compute_location(f)
    scale = compute_scale(f, location)

    approximation = lambda x: norm.pdf(x, location, scale)

    xs = np.linspace(-3, 3, 100)
    plt.plot(xs, [f(x) for x in xs], label="original")
    plt.plot(xs, [approximation(x) for x in xs], label="approximation")
    plt.legend()
    plt.show()


main()
