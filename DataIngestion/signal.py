import numpy as np


def detect_edge_shock(
    coefs:        np.ndarray,        # shape (n_scales, n_times)
    periods:      np.ndarray,        # shape (n_scales,), in hours
    max_period:   float = 4.0,       # only inspect rows at or below this
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
    A 2D boolean matrix of shape (len(scales), signal_length). 
    True means the data is corrupted. False means the data is safe.

    """

    results = coefs[2:max_period+1]
    standard_dev = (np.std(results, axis=1))
    


