import pickle
import re
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# import data
emg_df = pd.read_csv(r'/home/spencelab/Documents/smart_pros/hand_jupyter_notebook/emg_hold_cup.csv')
#print(emg_rest)
#sc = StandardScaler()
x = emg_df.drop('label', axis=1)
y = emg_df['label']
h = 0.02

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

'''
# perform lda
lda = LinearDiscriminantAnalysis(n_components=2)
x_train_lda = lda.fit_transform(x_train, y_train)

train_data_lda = pd.DataFrame(x_train_lda)
train_data_lda['label'] = y_train
train_data_lda.columns = ['LD1', 'LD2', 'label']

train_data_lda.head()
'''
# PCA
'''
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

pca = PCA(n_components=2)
x_train = pca.fit_transform(x_train)
x_test = pca.fit_transform(x_test)

print(pca.explained_variance_ratio_)
# initialize x and y
'''
# SVM training session

C = 1.0
#clf_rbf = svm.SVC(kernel='rbf')
svc = svm.SVC(kernel='linear', C=C).fit(x_train, y_train)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(x_train, y_train)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(x_train, y_train)


'''
x_min, x_max = x_train[:, 0].min() - 1, x_train[:, 0].max() + 1
y_min, y_max = x_train[:, 1].min() - 1, x_train[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))


titles = ['SVC with linear kernel',
          'LinearSVC (linear kernel)',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel']

for i, clf in enumerate((svc, lin_svc, rbf_svc, poly_svc)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot also the training points
    plt.scatter(x_train[:, 0], x_train[:, 1], c=y, cmap=plt.cm.coolwarm)

    #plt.xlabel('Sepal length')
    #plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])

plt.show()
'''
# save svm model
filename = 'emg_svm_model.pkl'
pickle.dump(rbf_svc, open(filename, 'wb'))
