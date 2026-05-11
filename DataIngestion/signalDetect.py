from typing import Any


import numpy as np


def detect_edge_shock(
    coefs:        np.ndarray,        # shape (n_scales, n_times)
    periods:      np.ndarray,        # shape (n_scales,), in hours
    max_period:   int = 4,           # only inspect rows at or below this
    k:            float = 3.0,
) -> bool:

    
    """
    Determines wether current prices are experiencing a downwards

    Parameters
    ----------
    coefs : np.ndarray
        The values after preforming Wavelet on price
    periods : np.ndarray
        The timescale or the number of scales
    max_period : int
        The max scale that will be checked
    k: int
        Arbitrary value for checking if it has passed shock treshold 

    Returns
    -------
    
    Returns an integer value for the minimum scale that triggered
    a shock

    """
    valid_period_mask = (periods >= 2) & (periods <= max_period)
    results = coefs[valid_period_mask]
    tracked_scales = periods[valid_period_mask]
    standard_dev = (np.std(results, axis=1))
    scaled_dev = standard_dev*k*-1
    last_column = results[:, -1]
    last_column_squeezed = np.squeeze(last_column)
    shock = scaled_dev > last_column_squeezed
    
    triggering_scales = tracked_scales[shock]

    if len(triggering_scales) == 0:
        return -1
    else:
        return np.min(triggering_scales)


