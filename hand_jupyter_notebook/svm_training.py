import pickle
import re
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# import data
emg_df = pd.read_csv(r'/home/thangvle/Desktop/github/smart_pros/hand_jupyter_notebook/emg_hold_cup.csv')
#print(emg_rest)
sc = StandardScaler()
x = emg_df.drop('label', axis=1)
y = emg_df['label']

# performing pca to reduce dataframe dimension
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

pca = PCA(n_components=2)
x_train = pca.fit_transform(x_train)
x_test = pca.fit_transform(x_test)

print(pca.explained_variance_ratio_)
# initialize x and y

# SVM training session

clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)

print(x_train)
y_pred = clf.predict(y)
#print(x_test)
print(y_pred)
'''
X_set, y_set = x_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1,
                     stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1,
                     stop = X_set[:, 1].max() + 1, step = 0.01))

plt.contourf(X1, X2, clf.predict(np.array([X1.ravel(),
             X2.ravel()]).T).reshape(X1.shape), alpha = 0.75,
             cmap = ListedColormap(('yellow', 'aquamarine')))

plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)

plt.title('SVM (Training set)')
plt.xlabel('PC1') # for Xlabel
plt.ylabel('PC2') # for Ylabel
plt.legend() # to show legend

# show scatter plot
plt.show()
'''
