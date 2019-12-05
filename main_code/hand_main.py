# this code will write serial input to arduino to control the LED
import pickle
import re
import serial
import pandas as pd
import numpy as np

# machine learning package
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

#from tqdm import tqdm_notebook as tqdm

# data visualization
import  seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

arduino_reader = serial.Serial('/dev/cu.usbmodem14502',115200,timeout=1)
arduino_command = serial.Serial('/dev/cu.usbmodem14502',115200,timeout=1)
# initialize a list to hold data

'''
mode 4 real time prediction
mode 1 grasp 1
mode 2 grasp 2
mode 3 rest
'''

idle = np.array([0,0,0,0,0,0])
pinch = np.array([0,0,0,0,0,1])
grip = np.array([0,0,0,0,0,2])
rest = np.array([0,0,0,0,0,3])
prediction = np.array([0,0,0,0,0,4])    # signal prediction mode
training = np.array([0,0,0,0,0,0,5])    # signal training mode
label = ['1','2','3','4']

df = pd.DataFrame(columns=['x', 'y','z','muscle1','muscle2','muscle3'])
raw_input = arduino.readline()  # read input from arduino
time.sleep(1)   # skip the first few bad data

def data_collection(df):
    while(1):
        raw_input = arduino.readline()      # actual arduino reading

        input_decoded = raw_input.decode()  # decode raw data to string
        # converting string to float
        data = np.array([x for x in input_decoded.rstrip().split("\t")], dtype=np.float32)

        # detect training / prediction mode

        df = df.append(pd.Series([data[0], data[1], data[2], data[3], data[4], data[5]], index=df.columns), ignore_index=True)
        last_row = df.tail(1).values
        if (np.array_equal(last_row, idle)):
            # delete last row of [0,0,0,0,0,0]
            df.drop(df.tail(1).index, inplace=True)
        if (np.array_equal(last_row, training)):
            if (np.array_equal(last_row, pinch)):
                # pinch mode
                df = df.assign(label=['1'])
            elif (np.array_equal(last_row, grip)):
                # grip mode
                df = df.assign(label=['2'])
            elif (np.array_equal(last_row, rest)):
                # rest mode
                df = df.assign(label=['3'])
            svm_training(df)
        if (np.array_equal(last_row, prediction)):
            # predict function
            predict(df)

def svm_training(emg_df):
    # fix the dataframe by using it as dataframe function paramters
    x = emg_df.drop('label', axis=1)
    y = emg_df['label']
    h = 0.02

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

    # initialize scaler
    sc = StandardScaler()
    x_train_scale = sc.fit_transform(x_train)
    x_test_scale = sc.fit_transform(x_test)

    # pca for dimentional reduction
    pca = PCA(n_components=2)
    x_train_pca = pca.fit_transform(x_train_scale, y_train)
    x_test_pca = pca.fit_transform(x_test_scale)
    train_data_pca = pd.DataFrame(x_train_pca)
    train_data_pca['label'] = y_train
    train_data_pca.columns = ['PCA1', 'PCA2', 'label']

    C = 1.0
    #clf_rbf = svm.SVC(kernel='rbf')
    #svc = svm.SVC(kernel='linear', C=C).fit(x_train, y_train)
    rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(x_train_pca, y_train)
    #poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(x_train, y_train)

    #y_pred = rbf_svc.predict(x_test_pca)
    #print(x_test_pca)
    #print(y_pred)

    # save model
    filename = 'emg_svm_model.pkl'
    pickle.dump(rbf_svc, open(filename, 'wb'))
    print('svm model saved')

# make prediction base on emg dataframe
def prediction(df, filename):
    while(1):

        emg_model = pickle.load(open(filename, 'rb'))
        raw_input = arduino_reader.readline()      # actual arduino reading

        input_decoded = raw_input.decode()  # decode raw data to string
        # converting string to float
        data = np.array([x for x in input_decoded.rstrip().split("\t")], dtype=np.float32)

        # attach the data to the dataframe
        # does the dataframe change when append new data?

        df = df.append(pd.Series([data[0], data[1], data[2], data[3], data[4], data[5]], index=df.columns), ignore_index=True)
        print(df.tail(1))
        mode = emg_model.predict(df.tail(1))
        print(mode)

        if(mode == "1"):
            arduino_command.write(b'H')
        if(mode == "2"):
            arduino_command.write(b'G')
        if(mode == "3"):
            arduino_command.write(b'R')

def main():
    filename = "/Users/nhok2303/Desktop/github/smart_pros/main_code/emg_svm_model.pkl"
    data_collection(df)
    svm_training(df)
    prediction(df, filename)


# initialize main function
if __name__ == "__main__":
    main()

'''
df.to_csv(r'/Users/nhok2303/Desktop/github/smart_pros/main_code/emg_with_label.csv')
print("saved to emg_with_label.csv")
'''

'''
for i in range(5):
    arduino.write(b'H')
    time.sleep(1)
    arduino.write(b'L')
    time.sleep(1)
# export to csv. Comment t variables. Maximum is 2048 his code out if not need to
'''
'''
        y_pred = svm_clf.predict(df)
        print(y_pred)
        for i in y_pred:
            if i == 'rest':
                arduino.write(b'R')
            elif i == 'active':
                arduino.write(b'A')

'''


#df = pd.DataFrame()

#plt.plot(cleandata)
#plt.show()



'''
while(input != None):
    raw_input = arduino.readline()
    #print((input))
    # read digit only input from arduino
    input_decoded = input.decode()
    input_formatted = input_decoded.rstrip()

    #flt = float(input_formatted)
    #print(input_decoded)
    #print(flt)
    #print(digit_array.shape)
    #print(digit_array.shape)

    #data_array = np.append(data_array, [digit_array], axis=0)
arduino.close()
'''
#plt.plot(digit_array)
#plt.show()
    #print(data_array)
    #for line in data:
    #    print(line)
    #create dataframe from data_array
    #df = pd.DataFrame()
#print()

    #df.head(10)

    #svm_clf.predict(digit)
