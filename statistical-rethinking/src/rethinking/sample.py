import numpy as np


def draw(xs, ys, n):
    """Draw a sample from a grid approximated distribution.

    :param xs: The grid.
    :param ys: The value of the pdf at the points of the grid.
    :param n: The number of samples.
    :returns: A list of samples.
    """
    heights = (ys[1:] + ys[:-1]) / 2
    widths = xs[:-1] - xs[1:]
    volumes = heights * widths
    stairs = np.cumsum(volumes) - volumes[0]
    for _ in range(n):
        i = np.argmax(np.random.uniform(0, stairs[-1]) > stairs)
        yield xs[i]
