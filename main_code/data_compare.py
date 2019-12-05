import pickle
import re
import pandas as pd
import numpy as np

emg_df = pd.read_csv(r'/home/spencelab/Documents/smart_pros/hand_jupyter_notebook/emg_hold_cup.csv')
# rm label from emg data frame
x = emg_df.drop('label', axis=1)
# extract the last row
last_row = x.tail(1).values
#print(type(last_row))
idleAnalog = np.array([0, 0, 0, 0, 0, 0])
#idletest = pd.DataFrame(idleAnalog)
if (np.array_equal(last_row,idleAnalog)):
    print("Idle Analog")
else:
    print("pass")
