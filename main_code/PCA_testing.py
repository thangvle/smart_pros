import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

emg_acc = pd.read_csv(r"/home/camera/Documents/smart_pros/hand_jupyter_notebook/emg_acc.csv")


features = ['x', 'y', 'z', 'muscle1', 'muscle2', 'muscle3']
# getting values
x = emg_acc.loc[:, features].values
# getting labels. Currently blank because there is no label

# scaling features
x = StandardScaler().fit_transform(x)

# setting the number of dimension of dataframe
pca = PCA(n_components=2)

pca_transform = pca.fit_transform(x)

pca_df = pd.DataFrame(data=pca_transform, columns=['pca1', 'pca2'])

print(pca_df)
print(pca.explained_variance_ratio_)
