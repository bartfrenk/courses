from collections import Counter

import numpy as np
import pymc3 as pm
import arviz as az
import pandas as pd

from rethinking.plot import plot_from_sample


class ModelExpr:
    def __init__(self, target, terms, df=None):
        if df is not None:
            errors = []
            if target not in df.columns:
                errors.append(f"Target {target} not in data frame")
            for var in self._variables(terms):
                if var not in df.columns:
                    errors.append(f"Variable {var} not in data frame")
            if errors:
                raise ValueError(errors)
        self.target = target
        self.terms = terms

    @staticmethod
    def _variables(terms):
        seen = set()
        for term in terms:
            for var in term:
                if var not in seen:
                    yield var
                seen.add(var)

    @property
    def variables(self):
        return list(self._variables(self.terms))

    @classmethod
    def from_str(cls, s, **kwargs):
        return cls(*cls._parse_expr(s), **kwargs)

    @classmethod
    def _parse_expr(cls, s):
        parts = s.split("=")
        if len(parts) == 2:
            target = parts[0].strip()
            terms = cls._parse_terms(parts[1])
            return (target, terms)
        raise ValueError(f"Invalid expression {s}")

    @classmethod
    def _parse_terms(cls, s):
        return list(map(cls._parse_summand, s.strip().split("+")))

    @classmethod
    def _parse_factor(cls, s):
        parts = s.strip().split("^")
        if len(parts) == 1:
            return [parts[0].strip()]
        if len(parts) == 2:
            return int(parts[1].strip()) * [parts[0].strip()]
        raise ValueError(f"Invalid factor {s}")

    @classmethod
    def _parse_summand(cls, s):
        summand = []
        for variables in map(cls._parse_factor, s.strip().split("*")):
            summand.extend(variables)
        return summand

    def __repr__(self):
        parts = []
        for term in self.terms:
            counts = Counter()
            for variable in term:
                counts[variable] += 1
            s = "*".join(f"{v}" if e == 1 else f"{v}^{e}" for (v, e) in counts.items())
            parts.append(s)
        return f"{self.target} = {' + '.join(parts)}"

    def values(self, df):
        return (df[self.target].values, design_matrix(df, self))

    def model(self, df):
        return create_model(*self.values(df))


def design_matrix(df, expr):
    columns = []
    for term in expr.terms:
        c = np.ones((len(df), 1))
        for variable in term:
            c *= df[variable].values.reshape((-1, 1))
        columns.append(c)
    return np.concatenate(columns, axis=1)


def create_model(y, X):
    m = pm.Model()
    n = X.shape[1]
    with m:
        intercept = pm.Normal("intercept", mu=0, sd=100)
        terms = pm.Normal("terms", mu=0, sd=100, shape=n)
        sd = pm.Uniform("sd", lower=0, upper=100)
        mu = intercept + pm.math.dot(X, terms)
        pm.Normal("y", mu=mu, sd=sd, observed=y)
    return m


def compute_aikake_weights(waics):
    exps = np.exp(0.5 * waics)
    return exps / np.sum(exps)


def compare_models(traces, exprs):
    waics = []
    models = []
    for (expr, trace) in zip(exprs, traces):
        waics.append(az.waic(trace))
        models.append(str(expr))
    measures = pd.DataFrame(
        {
            "model": models,
            "waic": [w.waic for w in waics],
            "p_waic": [w.p_waic for w in waics],
        }
    )
    measures["dwaic"] = np.max(measures.waic) - measures.waic
    measures["aikake_weights"] = compute_aikake_weights(measures.waic.values)
    return measures


def sample_model(expr, trace, n, **terms):
    df = pd.DataFrame()
    constants = {}
    for (name, values) in terms.items():
        if not isinstance(values, (list, np.ndarray)):
            constants[name] = values
        else:
            df[name] = values
            xs = values
    for (name, value) in constants.items():
        df[name] = value
    X = design_matrix(df, expr)
    indices = np.random.choice(range(len(trace["intercept"])), size=n)
    intercept = trace["intercept"][indices]
    terms = trace["terms"][indices].transpose()
    return (xs, intercept + np.dot(X, terms))


def sample_mixture(exprs, traces, n, ps, **terms):
    counts = np.random.multinomial(n, pvals=ps)
    samples = []
    for (expr, trace, count) in zip(exprs, traces, counts):
        (xs, yss) = sample_model(expr, trace, n=count, **terms)
        samples.append(yss)
    return (xs, np.hstack(samples))


def plot_lm(ax, expr, trace, *, n=10000, **terms):
    (xs, yss) = sample_model(expr, trace, n, **terms)
    plot_from_sample(xs, yss, ax=ax, label=str(expr))


if __name__ == "__main__":
    print(ModelExpr.from_str("y = x * X * x + z * x * X^100"))
