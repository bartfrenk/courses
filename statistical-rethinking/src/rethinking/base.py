from collections import namedtuple
import numpy as np


_Interval = namedtuple("_Interval", ["lo", "hi"])


class Interval(_Interval):
    @property
    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"


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


def hdpi(p, sample, sorted=False):
    """Estimate a HDPI from a sample

    :param p: The fraction to include in the HDPI.
    :param sample: The sample.
    :param sorted: Whether the sample is already sorted.
    :returns: The HDPI of class :class:`~Interval`.
    """
    zs = sorted(sample) if not sorted else sample
    n = len(zs)
    m = round(p * n)
    chosen = Interval(zs[0], zs[m - 1])
    for i in range(1, n - m):
        candidate = Interval(zs[i], zs[i + m - 1])
        if candidate.width < chosen.width:
            chosen = candidate
    return chosen
