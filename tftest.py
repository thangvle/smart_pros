import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# load training data
data = keras.datasets.fashion_mnist
# split data into train and test
(train_imgs, train_labels), (test_imgs, test_labels) = data.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
train_imgs = train_imgs/255.0
test_imgs = test_imgs/255.0

# creating modelx

model = keras.Sequential([
                keras.layers.Flatten(input_shape=(28,28)),      # flatten the img from 2D to 1D array
                keras.layers.Dense(128, activation="relu"),     # activation function layers
                keras.layers.Dense(10, activation="softmax")    #
                ])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])
# fitting the model to the data
model.fit(train_imgs, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_images, test_labels)

prediction = model.predict(test_imgs)
print(np.argmax(class_names[prediction[0]]))
