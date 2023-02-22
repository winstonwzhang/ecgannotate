
import numpy as np
import scipy
import os

infolder = 'example_data/'

for file in os.listdir(infolder):
    if file.endswith('.mat'):
        infile = os.path.join(infolder,file)
        outfile = os.path.join(infolder,file[:-4]+'.npy')

        ecg = scipy.io.loadmat(infile)
        ecg = ecg['ecg']
        np.save(outfile, ecg)