
# coding: utf-8

# SVM tutorial 
# 
# https://www.datacamp.com/community/tutorials/svm-classification-scikit-learn-python

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle


# In[2]:


cup_df = pd.read_excel(r"/home/camera/Documents/smart_pros/hand_jupyter_notebook/hold_a_cup.xlsx", sheet_name="force2")

cup_df.head(10)



# In[3]:



cup_df.columns = ['raw_time', 'time', 'muscle_1', 'muscle_2', 'muscle_3', 'muscle_4', 'muscle_5', 'mode']
cup_df = cup_df.drop('raw_time',1)
cup_df = cup_df.drop(0)




# In[5]:


cup_df


# In[4]:


f, (ax1) = plt.subplots(1,1, figsize=(12,5))
ax1.scatter(x=cup_df['time'], y=cup_df['muscle_3'], marker="s")


'''
ax2.scatter(x=cup_df['time'], y=cup_df['muscle_2'])
ax3.scatter(x=cup_df['time'], y=cup_df['muscle_3'])
ax4.scatter(x=cup_df['time'], y=cup_df['muscle_4'])
ax5.scatter(x=cup_df['time'], y=cup_df['muscle_5'])
'''
plt.show()


# In[6]:


x = cup_df.drop('mode', axis=1)
y = cup_df['mode']

print(x)


# In[8]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)
clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)

print(x_train)


# In[9]:


x_train.shape


# In[10]:


test=cup_df[:5].drop('mode',axis=1)
#print(test)
y_pred = clf.predict(test)
print(y_pred)




# In[47]:


print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))


# In[13]:


force3 = pd.read_excel(r"/home/camera/Documents/smart_pros/hand_jupyter_notebook/hold_a_cup.xlsx", sheet_name="force3")
force3.head()


# In[14]:


force3.columns = ['raw_time', 'time', 'muscle_1', 'muscle_2', 'muscle_3', 'muscle_4', 'muscle_5']
force3 = force3.drop('raw_time',1)
force3 = force3.drop(0)


# In[15]:


force3.head()


# In[18]:


force3_sample = force3[:1]
y_pred = clf.predict(force3_sample)
print(y_pred)


# In[19]:


force3_sample.shape


# In[ ]:


filename = 'EMG_svm_pickle.pkl'
EMG_svm_pickle = open(filename, "wb")
pickle.dump(clf, EMG_svm_pickle)
EMG_svm_pickle.close()

