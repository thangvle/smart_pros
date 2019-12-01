import numpy as np
import pandas as pd
import gumpy.Dataset


import matplotlib.pyplot as plt
import sys, os, os.path

base_dir = '../..'
subject = 'S2'
data_low = gumpy.nst_emg.NST_EMG(base_dir, subject, 'low')
data_high = gumpy.nst_emg.NST_EMG(base_dir, subject, 'high')

# Finally, load the dataset
data_low.load()
data_high.load()

print(data_low)
