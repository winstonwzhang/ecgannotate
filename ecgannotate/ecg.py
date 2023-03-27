

import numpy as np

from ecgdetectors import Detectors



def findPeaks(fs, ecg):
    # Initialize the detectors object
    detectors = Detectors(fs)

    # Use the Pan-Tompkins algorithm to detect R-peaks
    r_peaks = detectors.pan_tompkins_detector(ecg)
    
    # r peaks returned as list of indices
    return r_peaks
    

def calculateHR(r_peaks, fs, w_start, w_end):
    """Calculate the heart rate from R-peaks detected within the start and end of current window.

    Args:
        r_peaks (numpy array): An array of R-peak indices.
        fs (float): The sampling frequency of the ECG signal.
        w_start (int): Start of current window (index).
        w_end (int): End of current window (index).

    Returns:
        float: Heart rate in current window.

    """
    # Calculate the duration of the window in seconds
    window_duration = (w_end - w_start) / fs

    # Count the number of R-peaks in the window using boolean indexing
    r_peaks_in_window = np.count_nonzero((r_peaks >= w_start) & (r_peaks <= w_end))

    # Calculate the heart rate in bpm
    heart_rate = r_peaks_in_window / window_duration * 60

    return heart_rate