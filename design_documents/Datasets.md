
## ECGannotate

# Dataset

MIT-BIH dataset publicly available on Physionet https://physionet.org/content/mitdb/1.0.0/

Converted to Matlab and numpy file format using Physionet-provided functions.

# Real dataset for answering a biological question using the tool

The dataset contains 48 half-hour 2-channel ECG records from 47 individual subjects. Sampling rate is 360 samples per second with cardiologist arrhythmia annotations available for each record. The raw ECG signals are readable into Python using the "pandas" module since the dataset is in .csv format.

The ECG signals are readable into Python and thus are valid input data for testing the developed ECG GUI in Python code.

We want to see if the GUI can successfully load ECG data from this public database. We also want to try to calculate heart rate statistics while viewing certain sections of the ECG signal. We expect to be able to view chunks of time series signal from an individual patient, and be able to calculate heart rate statistics for certain sections of time. We also should be able to add annotations to a time window and view added annotations in a table format.