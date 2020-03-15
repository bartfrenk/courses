import numpy as np


def normalize(ws):
    def fn(xs):
        return (xs - np.mean(ws)) / np.std(ws)

    return fn
