# -*- coding: utf-8 -*-
"""cactus_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ePT9OXk_R5--x1EzY5VvSud-nY9u8V8C
"""

## connecting notebook to google drive
# click on the URL, give permissions and copy and paste the authorisation code to connect
from google.colab import drive
drive.mount('/gdrive')

# make sure to place the folder in the main section of your google drive to connect to this folder

import os
os.chdir('/gdrive/My Drive/Cactus')

# !pip3 install kaggle==1.5.6
# !kaggle -v
# !mkdir .kaggle
# !echo '{"username":"krbarks","key":"1cecf711ae1108eecb69ce6380d6fec7"}' > /root/.kaggle/kaggle.json
# !chmod 600 /root/.kaggle/kaggle.json

# get data from https://www.kaggle.com/c/aerial-cactus-identification/
# ! kaggle competitions download -c aerial-cactus-identification

# unzip data
# !unzip train.zip
# ! unzip test.zip

import os

os.listdir()

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import imageio
import os
import PIL
import cv2

# %tensorflow_version 1.x

import keras
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model

train_label = pd.read_csv('train.csv')
sample_submission = pd.read_csv('sample_submission.csv')

train_label.head()

sample_submission.head()

## code to sort the training labels to the image arrays
# filenames = glob.glob('*.*')

# sorted_cactus = ["a"]*len(filenames)

# for i in range(len(filenames)):
#   for j in range(len(train_label)):
#     if filenames[i] == train_label["id"][j]:
#       sorted_cactus[i] = train_label["has_cactus"][j]

# d = {'id': filenames, 'has_cactus': sorted_cactus}
# labels_sort = pd.DataFrame(data=d)

# labels_sort.to_csv("train_label_sorted.csv")

labels_sort.head()

## DO NOT RUN THIS BLOCK ##
# you can load the images with the script in the next block, it will be much quicker
# standardised image size
# IMAGE_SIZE = (32, 32)

# train_img = []

# index = 0
# # function to resize and reshape the RGB images into arrays
# for index, filename in enumerate(glob.glob('train/*.*')):
#     '''
#     For loop that pre-processes JPG images
#     '''
#     image = imageio.imread(filename)
#     # resize data to reduce size for model efficiency
#     image = cv2.resize(image, IMAGE_SIZE)
#     image = np.array(image)
#     # ensure all data has the same shape
#     #if np.shape(image) == (32, 32, 3):
#     train_img.append(image)
#     index += 1
#     if index%1000 == 0:
#       print(index)

## load numpy arrays below rather than the images above for faster loading

train_img = np.load('train_img.npy')
train_data = np.load('train_data.npy')
eval_data = np.load('eval_data.npy')

print(len(train_img))

plt.imshow(train_img[150])

# sample = int(17500*0.25)
# print(sample)
# eval_data = train_img[:sample]
# train_data = train_img[sample:]

# # convert to array
# train_data = np.array(train_data)
# eval_data = np.array(eval_data)

# pre-processing the data

# train_data = train_data.astype('float32') / 255.
# eval_data = eval_data.astype('float32') / 255.
# train_data = train_data.reshape((len(train_data), np.prod(train_data.shape[1:])))
# eval_data = eval_data.reshape((len(eval_data), np.prod(eval_data.shape[1:])))

# np.save("train_img", train_img)
# np.save("train_data", train_data)
# np.save("eval_data", eval_data)

eval_data = eval_data.reshape(4375, 32, 32, 3)
train_data = train_data.reshape(13125, 32, 32, 3)
test_data = eval_data[:int(4375/2)]
eval_data = eval_data[int(4375/2):]

# autoencoder

# this is our input placeholder
input_img = Input(shape=(32, 32, 3))  

## ENCODER ##
# Conv1 #
encoded = Conv2D(filters = 256, kernel_size = (3, 3), activation='relu', padding='same')(input_img)
encoded = Conv2D(filters = 256, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded)
print(encoded.shape)

# Conv2 #
encoded = Conv2D(filters = 128, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = Conv2D(filters = 128, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded)
print(encoded.shape)

# Conv3 #
encoded = Conv2D(filters = 64, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = Conv2D(filters = 64, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded)
print(encoded.shape)

# Conv4 #
encoded = Conv2D(filters = 32, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = Conv2D(filters = 32, kernel_size = (3, 3), activation='relu', padding='same')(encoded)
encoded = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded)
print(encoded.shape)


## DECODER ##

# DeConv1
decoded = Conv2D(32, (3, 3), activation='relu', padding='same')(encoded)
decoded = Conv2D(32, (3, 3), activation='relu', padding='same')(decoded)
decoded = UpSampling2D((2, 2))(decoded)
print(decoded.shape)

# DeConv2
decoded = Conv2D(64, (3, 3), activation='relu', padding='same')(decoded)
decoded = Conv2D(64, (3, 3), activation='relu', padding='same')(decoded)
decoded = UpSampling2D((2, 2))(decoded)
print(decoded.shape)

# DeConv3
decoded = Conv2D(128, (3, 3), activation='relu', padding='same')(decoded)
decoded = Conv2D(128, (3, 3), activation='relu', padding='same')(decoded)
decoded = UpSampling2D((2, 2))(decoded)
print(decoded.shape)

# DeConv4
decoded = Conv2D(256, (3, 3), activation='relu', padding='same')(decoded)
decoded = Conv2D(256, (3, 3), activation='relu', padding='same')(decoded)
decoded = UpSampling2D((2, 2))(decoded)
print(decoded.shape)

decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(decoded)
print(decoded.shape)


## ENCODER and AUTOENCODER ##

autoencoder = Model(input_img, decoded)
encoder = Model(input_img, encoded)

autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

autoencoder.fit(train_data, train_data,
                epochs=1000,
                batch_size=256,
                shuffle=True,
                validation_data=(eval_data, eval_data))

# visualising the autoencoder

reconst_test = autoencoder.predict(eval_data)

n = 10
row = 2

plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(row, n, i + 1)
    plt.imshow(eval_data[i].reshape(32, 32, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(row, n, i + 1 + n)
    plt.imshow(reconst_test[i].reshape(32, 32, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
plt.show()

# saving whole model
autoencoder.save('autoencoders/autoencoder_model1.h5')
 
# loading whole model
model1 = load_model('autoencoders/autoencoder_model1.h5')

encoder.save('autoencoders/encoder_model1.h5') # forgot to run this

# Plot training & validation loss values

plt.figure(figsize=(10, 6))
plt.plot(autoencoder.history.history['loss'])
plt.plot(autoencoder.history.history['val_loss'])
plt.title('Autoencoder loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

# autoencoder

# this is our input placeholder
input_img_2 = Input(shape=(32, 32, 3))  

## ENCODER ##
# Conv1 #
encoded_2 = Conv2D(filters = 256, kernel_size = (3, 3), activation='relu', padding='same')(input_img_2)
encoded_2 = Conv2D(filters = 256, kernel_size = (3, 3), activation='relu', padding='same')(encoded_2)
encoded_2 = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded_2)
print(encoded_2.shape)

# Conv2 #
encoded_2 = Conv2D(filters = 128, kernel_size = (3, 3), activation='relu', padding='same')(encoded_2)
encoded_2 = Conv2D(filters = 128, kernel_size = (3, 3), activation='relu', padding='same')(encoded_2)
encoded_2 = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded_2)
print(encoded_2.shape)

# Conv3 #
encoded_2 = Conv2D(filters = 64, kernel_size = (3, 3), activation='relu', padding='same')(encoded_2)
encoded_2 = Conv2D(filters = 64, kernel_size = (3, 3), activation='relu', padding='same')(encoded_2)
encoded_2 = MaxPooling2D(pool_size = (2, 2), padding='same', strides=2)(encoded_2)
print(encoded_2.shape)

## DECODER ##

# DeConv1
decoded_2 = Conv2D(64, (3, 3), activation='relu', padding='same')(encoded_2)
decoded_2 = Conv2D(64, (3, 3), activation='relu', padding='same')(decoded_2)
decoded_2 = UpSampling2D((2, 2))(decoded_2)
print(decoded_2.shape)

# DeConv2
decoded_2 = Conv2D(128, (3, 3), activation='relu', padding='same')(decoded_2)
decoded_2 = Conv2D(128, (3, 3), activation='relu', padding='same')(decoded_2)
decoded_2 = UpSampling2D((2, 2))(decoded_2)
print(decoded_2.shape)

# DeConv3
decoded_2 = Conv2D(256, (3, 3), activation='relu', padding='same')(decoded_2)
decoded_2 = Conv2D(256, (3, 3), activation='relu', padding='same')(decoded_2)
decoded_2 = UpSampling2D((2, 2))(decoded_2)
print(decoded_2.shape)

decoded_2 = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(decoded_2)
print(decoded_2.shape)


## ENCODER and AUTOENCODER ##

autoencoder_2 = Model(input_img_2, decoded_2)
encoder_2 = Model(input_img_2, encoded_2)

autoencoder_2.compile(optimizer='adadelta', loss='binary_crossentropy')

autoencoder_2.fit(train_data, train_data,
                epochs=1000,
                batch_size=256,
                shuffle=True,
                validation_data=(eval_data, eval_data))

# visualising the autoencoder

reconst_test_2 = autoencoder_2.predict(eval_data)

n = 10
row = 2

plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(row, n, i + 1)
    plt.imshow(eval_data[i].reshape(32, 32, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(row, n, i + 1 + n)
    plt.imshow(reconst_test_2[i].reshape(32, 32, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
plt.show()

# Plot training & validation loss values

plt.figure(figsize=(10, 6))
plt.plot(autoencoder_2.history.history['loss'])
plt.plot(autoencoder_2.history.history['val_loss'])
plt.title('Autoencoder loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

autoencoder_2.save('autoencoders/autoencoder_model2.h5')
encoder_2.save('autoencoders/encoder_model2.h5')

from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler

pca_x = np.reshape(train_data, (24000,96))

scaler = StandardScaler()
scaler.fit(pca_x)
scaled_x = scaler.transform(pca_x)

pca = decomposition.PCA(.95)

pca_transformed = pca.fit_transform(scaled_x)

plt.plot(pca_transformed)
plt.title('PCA')
plt.show()

fig, axes = plt.subplots(2,10,figsize=(20,4),
 subplot_kw={'xticks':[], 'yticks':[]},
 gridspec_kw=dict(hspace=0.01, wspace=0.01))
for i, ax in enumerate(axes.flat):
    ax.imshow(pca.components_[i].reshape(12,8), cmap='gray')

pca.n_features_