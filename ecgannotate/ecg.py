

import numpy as np

from ecgdetectors import Detectors



def findPeaks(fs, ecg):
    # Initialize the detectors object
    detectors = Detectors(fs)

    # Use the Pan-Tompkins algorithm to detect R-peaks
    r_peaks = detectors.pan_tompkins_detector(ecg)
    
    # r peaks returned as list of indices
    return r_peaks
    

def calculateHR(num_peaks, fs, win_size):
    """Calculate the heart rate from R-peaks detected within the start and end of current window.
    """
    # Calculate the duration of the window in seconds
    window_duration = win_size / fs

    # Calculate the heart rate in bpm
    heart_rate = num_peaks / window_duration * 60

    return heart_rate