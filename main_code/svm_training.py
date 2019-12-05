# data preprocesing miscellanous packages
import pickle
import re
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

from tqdm import tqdm_notebook as tqdm

# data visualization
import  seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# import data
emg_df = pd.read_csv(r'/home/spencelab/Documents/smart_pros/main_code/emg_hold_cup.csv')
#print(emg_rest)
#sc = StandardScaler()
x = emg_df.drop('label', axis=1)
y = emg_df['label']
h = 0.02

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)


# perform lda


sc = StandardScaler()
x_train_lda = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

'''
lda = LDA(n_components=2)
x_train_lda = lda.fit_transform(x_train, y_train)
x_test_lda = lda.transform(x_test)

train_data_lda = pd.DataFrame(x_train_lda)
train_data_lda['label'] = y_train
train_data_lda.columns = ['LD1', 'LD2', 'label']
'''


# PCA

x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

pca = PCA(n_components=2)
x_train_pca = pca.fit_transform(x_train, y_train)
x_test_pca = pca.fit_transform(x_test)
train_data_pca = pd.DataFrame(x_train_pca)
train_data_pca['label'] = y_train
train_data_pca.columns = ['PCA1', 'PCA2', 'label']

print(pca.explained_variance_ratio_)
# initialize x and y

# SVM training session

C = 2.0
#clf_rbf = svm.SVC(kernel='rbf')
#svc = svm.SVC(kernel='linear', C=C).fit(x_train, y_train)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(x_train_pca, y_train)
#poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(x_train, y_train)

y_pred = rbf_svc.predict(x_test_pca)
print(x_test_pca)
print(y_pred)
#print(rbf_svc.support_vectors_)



# visualization

def plot_svm(model, ax = None, plot_support=True):
    if ax == None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # grid for evaluated model
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y,x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape()

    # plot decision boundary
    ax.contour(X, Y, P, colors='k', levels=[1, 0, 1], alpha = 0.95,)
    if plot_support:
        ax.scatter(model.support_vectors_[:,0],
                   model.support_vectors_[:,1],
                   s=300, linewidth=1, facecolors='none');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

markers = ['s', 'x','o']
colors = ['r', 'b','g']
#plot_svm(rbf_svc)
sns.lmplot(x="PCA1", y="PCA2", data=train_data_pca, hue='label', markers=markers,fit_reg=False,legend=False)
print(pca.explained_variance_ratio_)
plt.legend(loc='upper center')

plt.show()



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
print('svm model saved')
