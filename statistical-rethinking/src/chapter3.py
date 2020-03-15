# pylint: disable=unused-variable
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import yaml

# Exercises 3H

_Interval = namedtuple("_Interval", ["lo", "hi"])


class Interval(_Interval):
    @property
    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"


def sample(ps, fs, n):
    heights = (fs[1:] + fs[:-1]) / 2
    widths = ps[:-1] - ps[1:]
    volumes = heights * widths
    stairs = np.cumsum(volumes) - volumes[0]
    for _ in range(n):
        i = np.argmax(np.random.uniform(0, stairs[-1]) > stairs)
        yield ps[i]


def hdpi(p, xs, sorted=False):
    zs = sorted(xs) if not sorted else xs
    n = len(zs)
    m = round(p * n)
    chosen = Interval(zs[0], zs[m - 1])
    for i in range(1, n - m):
        candidate = Interval(zs[i], zs[i + m - 1])
        if candidate.width < chosen.width:
            chosen = candidate
    return chosen


def exercise_3H3(xs):
    (k, m) = (100000, 200)
    ps = np.linspace(0, 1, 1000)
    fs = posterior(xs, ps)
    probs = list(sample(ps, fs, k))
    births = np.random.binomial(m, p=probs, size=k)
    sns.distplot(births)


def exercise_3H2(xs):
    ps = np.linspace(0, 1, 1000)
    fs = posterior(xs, ps)
    samples = sorted(sample(ps, fs, 100000))
    fraction = [0.5, 0.89, 0.97]
    for p in fraction:
        interval = hdpi(p, samples, sorted=True)
        print(f"\t{p}\t{interval}\t{interval.width}")


def exercise_3H4(data):
    (k, m) = (100000, 200)
    xs = np.array(data["birth1"] + data["birth2"])
    ps = np.linspace(0, 1, 1000)
    fs = posterior(xs, ps)
    probs = list(sample(ps, fs, m))
    mean = np.mean(data["birth1"])
    print(f"3H4\tSample mean first borns: {mean}")


def data_3H():
    with open("data/3H.yaml") as h:
        return yaml.load(h, Loader=yaml.SafeLoader)


def likelihood_bernoulli(xs, p):
    return np.prod((p ** xs) * ((1 - p) ** (1 - xs)))


def likelihood_binomial(xs, p):
    n = len(xs)
    m = np.sum(xs)
    return (p ** m) * ((1 - p) ** (n - m))


def posterior(xs, ps):
    fs = np.array([likelihood_bernoulli(xs, p) for p in ps])
    return fs / np.sum(fs)


def exercise_3H1(xs):
    ps = np.linspace(0, 1, 1000)
    fs = posterior(xs, ps)
    i = np.argmax(fs)
    print(f"3H1\tSample mean: {np.mean(xs)}")
    print(f"3H1\tApproximate maximum at: {ps[i]}")


def exercise_3H5(data):
    selection = where_first_is_girl(data)
    mean = np.mean(selection["birth2"])
    print(f"3H5\tSample mean: {mean}")


def where_first_is_girl(data):
    selection = {"birth1": [], "birth2": []}
    for (i, is_boy) in enumerate(data["birth1"]):
        if is_boy == 0:
            selection["birth1"].append(0)
            selection["birth2"].append(data["birth2"][i])
    return selection


def main():
    data = data_3H()
    xs = np.array(data["birth1"] + data["birth2"])
    exercise_3H1(xs)
    exercise_3H2(xs)
    exercise_3H3(xs)
    exercise_3H4(data)
    exercise_3H5(data)
    plt.show()


if __name__ == "__main__":
    main()
