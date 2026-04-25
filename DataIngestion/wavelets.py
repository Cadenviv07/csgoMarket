import numpy as np
import pywt

def build_scales(min_period_hours, max_period_hours, n_scales) -> np.ndarray:

    """
    Calculates the scale width the wavelet will use.

    Parameters
    ----------
    min_period_hours : int
        The smallest width frame the wavelet will test
    max_period_hours : int
        The largest width frame the wavelet will test
    n_scales : int
        The amount of frames betwwen min and max to smooth heatmap gradient

    Returns
    -------
    np.ndarray
        A numpys array that holds the scales that will be used for the wavelet
    """

    human_hours = np.logspace(min_period_hours,max_period_hours, num=n_scales)

    ricker_scales = human_hours/3.97

    return ricker_scales


def compute_cwt(signal, scales) -> (coefficients, periods_in_hours):

    """
    Calculates the coefficent matrix using mexicanhat wavelet then normalizes
    it among all scales

    Parameters
    ----------
    signal : np.ndarray
        1D array of the logged momentum values for a case 
    scales : np.ndarray
        Array of scales the wavelet will use

    Returns
    -------
    np.ndarray
        A matrix of size len(scales), len(signal) that holds the normalied cofficent values
    """

    coefs, _ = pywt.cwt(signal,scales, 'mexh', sampling_period=1)

    normalized_coefs = coefs * (1/(np.sqrt(scales[:, None])))

    return normalized_coefs


