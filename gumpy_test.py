import numpy as np
import pandas as pd



import matplotlib.pyplot as plt
import sys, os, os.path

base_dir = '/home/spencelab/Documents/smart_pros/hand_jupyter_notebook/emg_hold_cup.csv'
df = pd.read_csv(base_dir)
# Finally, load the dataset
#data_low.load()
#data_high.load()

print(df)
window_size = 0.2
window_shift = 0.05
fs = 512
x1 = gumpy.signal.rms(df, fs, window_size, window_shift)
print(x1)
