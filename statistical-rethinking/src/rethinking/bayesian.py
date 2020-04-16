from rethinking.misc import Interval


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
