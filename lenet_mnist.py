# -*- coding: utf-8 -*-


from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras.datasets import mnist
import numpy as np
import keras
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.examples.tutorials.mnist import input_data

#Parameters
weight_decay = 0.0005
batch_size = 64
epochs = 200
data_augmentation = True


#  Dataset 
mnist = input_data.read_data_sets("MNIST_data/", reshape=False)
x_train, y_train           = mnist.train.images, mnist.train.labels
x_validation, y_validation = mnist.validation.images, mnist.validation.labels
x_test, y_test             = mnist.test.images, mnist.test.labels


y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)


# Model:
model = Sequential()

model.add(Convolution2D(
    filters = 20,
    kernel_size = (5, 5),
    padding = "same",
    input_shape = (28, 28, 1)))

model.add(Activation(
    activation = "relu"))


model.add(MaxPooling2D(
    pool_size = (2, 2),
    strides =  (2, 2)))

model.add(Convolution2D(
    filters = 50,
    kernel_size = (5, 5),
    padding = "same"))

model.add(Activation(
    activation = "relu"))


model.add(MaxPooling2D(
    pool_size = (2, 2),
    strides = (2, 2)))

model.add(Flatten())


model.add(Dense(500))

model.add(Activation(
    activation = "relu"))

model.add(Dense(10))


model.add(Activation("softmax"))


model.summary()

model.compile(loss='categorical_crossentropy', optimizer='sgd',metrics=['accuracy'])

# Data Augmentation

datagen = ImageDataGenerator( featurewise_center=False,  # set input mean to 0 over the dataset
                             samplewise_center=False,  # set each sample mean to 0
                             featurewise_std_normalization=False,  # divide inputs by std of the dataset
                             samplewise_std_normalization=False,  # divide each input by its std
                             zca_whitening=False,  # apply ZCA whitening
                             rotation_range=15,  # randomly rotate images in the range (degrees, 0 to 180)
                             width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
                             height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
                             horizontal_flip=True,  # randomly flip images
                             vertical_flip=False)  # randomly flip images

# Train Network
cnn = model.fit(datagen.flow(x_train, y_train, batch_size=batch_size),steps_per_epoch=x_train.shape[0] // batch_size,
                                  epochs=epochs, validation_data=(x_test, y_test),verbose=2)




plt.figure(0)
plt.plot(cnn.history['acc'],'r')
plt.plot(cnn.history['val_acc'],'g')
plt.xticks(np.arange(0, 11, 2.0))
plt.rcParams['figure.figsize'] = (8, 6)
plt.xlabel("Num of Epochs")
plt.ylabel("Accuracy")
plt.title("Training Accuracy vs Validation Accuracy")
plt.legend(['train','validation'])

plt.figure(1)
plt.plot(cnn.history['loss'],'r')
plt.plot(cnn.history['val_loss'],'g')
plt.xticks(np.arange(0, 11, 2.0))
plt.rcParams['figure.figsize'] = (8, 6)
plt.xlabel("Num of Epochs")
plt.ylabel("Loss")
plt.title("Training Loss vs Validation Loss")
plt.legend(['train','validation'])
plt.show()