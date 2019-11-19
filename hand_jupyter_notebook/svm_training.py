import pickle
import re
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# import data
emg_df = pd.read_csv(r'/home/camera/Documents/smart_pros/hand_jupyter_notebook/emg_hold_cup.csv')
#print(emg_rest)
x = emg_df.drop('label', axis=1)
y = emg_df['label']

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
pca_df = pd.DataFrame(data=principalComponents, columns = ['pca1', 'pca2'])
pca_label = pd.concat([pca_df, emg_df[['label']]], axis=1)
print(pca_label)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 Component PCA', fontsize = 20)


targets = ['x', 'y', 'z', 'muscle1', 'muscle2', 'muscle3']
colors = ['r', 'g', 'b', 'c', 'm', 'y']
for target, color in zip(targets,colors):
    indicesToKeep = pca_label['label'] == target
    ax.scatter(pca_label.loc[indicesToKeep, 'pca1']
               , pca_label.loc[indicesToKeep, 'pca2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
plt.show()



print(pca.explained_variance_ratio_)
# initialize x and y

# SVM training session
'''
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)
clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)

print(x_train)
y_pred = clf.predict(test)
print(y_pred)
'''
