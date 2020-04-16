from typing import Mapping, Any
import numpy as np
import arviz as az
import pandas as pd


def polynomial_design_matrix(xs, n):
    return np.repeat([xs], n, axis=0).transpose() ** range(1, n + 1)


Trace = Any


def compute_aikake_weights(waics):
    exps = np.exp(0.5 * waics)
    return exps / np.sum(exps)


def compare(m: Mapping[str, Trace]) -> pd.DataFrame:
    waics = []
    models = []
    for (expr, trace) in m.items():
        waics.append(az.waic(trace))
        models.append(str(expr))
    measures = pd.DataFrame(
        {"waic": [w.waic for w in waics], "p_waic": [w.p_waic for w in waics],}
    )
    measures.index = models
    measures["dwaic"] = np.max(measures.waic) - measures.waic
    measures["weights"] = compute_aikake_weights(measures.waic.values)
    measures.sort_values(by="dwaic", inplace=True)
    return measures
