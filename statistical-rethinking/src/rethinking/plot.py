import numpy as np
import scipy.stats as st


def plot_from_sample(xs, yss, ax, p=0.95, label=None, **kwargs):
    mu = np.mean(yss, axis=1)
    sd = np.sqrt(np.mean(yss ** 2, axis=1) - mu ** 2)
    z = st.norm.ppf((1 - p) / 2)
    ax.plot(xs, mu, color="black", linewidth=1, **kwargs)
    # Compute the confidence intervals based on a normal approximation
    # to the predictive posterior distribution at the grid points
    ax.fill_between(xs, mu - z * sd, mu + z * sd, label=label, alpha=0.5)
