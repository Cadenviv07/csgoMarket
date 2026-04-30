from turtle import distance
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

    human_hours = np.linspace(min_period_hours,max_period_hours, num=n_scales)

    ricker_scales = human_hours/3.97

    return ricker_scales


def compute_cwt(signal, scales) -> tuple[np.ndarray, np.ndarray]:

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

    clean_signal = np.asarray(signal, dtype=np.float64).flatten()
    clean_scales = np.asarray(scales, dtype=np.float64).flatten()

    coefs, _ = pywt.cwt(clean_signal,clean_scales, 'mexh', sampling_period=1, method='fft')

    #normalized_coefs = coefs * np.sqrt(ricker_scales[:, None])

    return coefs, scales*3.97

def cone_of_influence(signal_length, scales, sampling_period_hours) -> np.ndarray:

    """
    Creates 2d matrix boolean mask representing the cone of influence for wavelet.
    
    The values in the invalid range will be marker false.

    Parameters
    ----------
    signal_length : int
        The total number of hourly data points being measured
    scales : np.ndarray
        Array of scales the wavelet will use
    sampling_period_hours : int
        Time between data rows 

    Returns
    -------
    A 2D boolean matrix of shape (len(scales), signal_length). 
    True means the data is corrupted. False means the data is safe.

    """

    invalid_hours = np.sqrt(2) * scales * sampling_period_hours
    time_indices = np.arange(signal_length)
    distance_from_edge = np.minimum(time_indices, (signal_length - 1 ) - time_indices)

    coi_mask = distance_from_edge[np.newaxis, :] < invalid_hours[:, np.newaxis]

    return coi_mask


if __name__ == "__main__":

    signal_length = 500
    x = np.arange(signal_length)

    baseline = np.zeros(signal_length)


    center_time = 250
    sigma = 4
    expected_period = sigma*3.97

    time_shifted = x - center_time

    bump = (1 - (time_shifted / sigma)**2) * np.exp(-0.5 * (time_shifted / sigma)**2)

    synthetic_market = baseline + bump

    human_hours = np.linspace(4, 24, num=100)
    ricker_scales = human_hours / 3.97

    coeffs,_ = compute_cwt(synthetic_market, ricker_scales)


    max_index_flat = np.argmax(coeffs)

    max_row, max_col = np.unravel_index(max_index_flat, coeffs.shape)

    detected_time = max_col
    detected_width = human_hours[max_row]

    print(f"--- LABORATORY CALIBRATION TEST ---")
    print(f"INJECTED SHOCK: Time = Hour {center_time}, Width = ~{expected_period:.2f}h")
    print(f"DETECTED SHOCK: Time = Hour {detected_time}, Width = {detected_width:.2f}h")

