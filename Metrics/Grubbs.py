import numpy as np
import pandas as pd
from scipy import stats
from math import sqrt


__all__ = ['test']


def _check_type(data):
    if isinstance(data, np.ndarray):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif isinstance(data, list):
        return np.array(data)
    else:
        raise TypeError('')


def _get_target_index(data):
    relative_values = data - data.mean()
    return abs(relative_values).argmax()


def _get_g(data):

    target_index = _get_target_index(data)
    absolute_normalized_data = abs((data - data.mean()) / data.std())
    return absolute_normalized_data[target_index]


def _get_g_test(n, alpha):
    t = stats.t.isf(alpha / (2*n), n-2)
    g_test = ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))
    return g_test


def _test_once(data, alpha):
    target_index = _get_target_index(data)
    g = _get_g(data)
    g_test = _get_g_test(len(data), alpha)
    if g > g_test:
        return target_index
    return


def _delete_item(data, index):
    if isinstance(data, pd.Series):
        return data.drop(index)
    elif isinstance(data, np.ndarray):
        return np.delete(data, index)
    else:
        raise TypeError("")


def compute(data, alpha=0.95):
    data = _check_type(data)
    while True:
        target_index = _test_once(data, alpha)
        if target_index is None:
            break
        data = _delete_item(data, target_index)
    return data
