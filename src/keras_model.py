from __future__ import print_function
import gzip
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
import urllib
import matplotlib.image as mpimg
from PIL import Image
from mask_to_submission import *
from helpers import *

import code
import tensorflow.python.platform
import numpy
import tensorflow as tf


import keras
#from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img



NUM_CHANNELS = 3 # RGB images
PIXEL_DEPTH = 255
NUM_LABELS = 2
TRAINING_SIZE = 50
TESTING_SIZE = 50
VALIDATION_SIZE = 5  # Size of the validation set.
SEED = 66478  # Set to None for random seed.
BATCH_SIZE = 16 # 64
NUM_EPOCHS = 5
RESTORE_MODEL = False # If True, restore existing model instead of training a new one
RECORDING_STEP = 1000

# Set image patch size in pixels
# IMG_PATCH_SIZE should be a multiple of 4
# image size should be an integer multiple of this number!
IMG_PATCH_SIZE = 16


# Extract data into numpy arrays, divided into patches of 16x16
data_dir = 'data/'
train_data_filename = data_dir + 'training/images/'
train_labels_filename = data_dir + 'training/groundtruth/' 
test_data_filename = data_dir + 'test_set_images'

print('\nLoading training images')
x_train = extract_data(train_data_filename, TRAINING_SIZE, IMG_PATCH_SIZE,  'train')
#print(x_train[:10])

print('Loading training labels')
y_train = extract_labels(train_labels_filename, TRAINING_SIZE, IMG_PATCH_SIZE)

print('Loading test images\n')
x_test = extract_data(test_data_filename,TESTING_SIZE, IMG_PATCH_SIZE, 'test')
#print(x_test[:10])

print('Train data shape: ',x_train.shape)
print('Train labels shape: ',y_train.shape)
print('Test data shape: ',x_test.shape)


train_datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True)

test_datagen = ImageDataGenerator()

train_generator = train_datagen.flow(
	x=x_train, 
	y=y_train,
	batch_size = BATCH_SIZE
	)

validation_generator = test_datagen.flow(
    x=x_test,
    batch_size=BATCH_SIZE,
    )


# input image dimensions
img_rows, img_cols = 16, 16
input_shape = (img_rows, img_cols, 3) # eller 3 på siste, for RGB channels?

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape)) #32 is number of outputs from that layer, kernel_size is filter size, 
#model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.5))
model.add(Dense(NUM_LABELS, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=BATCH_SIZE,
          epochs=NUM_EPOCHS,
          shuffle = True,
          verbose=1,
          validation_split = 0.2)
          #validation_data=(x_test, y_test))
#score = model.evaluate(x_test, y_test, verbose=0)
#print('Test loss:', score[0])
#print('Test accuracy:', score[1])

y_submit = model.predict_classes(x_test)
print(y_submit.shape)
print(sum(y_submit))

image_filenames=[]
prediction_test_dir = "predictions_test/"
'''for i in range(1,TESTING_SIZE+1):
    test_data_filename = data_dir + 'test_set_images'

    filename = prediction_test_dir + "predictimg_" + str(i) + ".png"
    imgpred = get_predictionimage(test_data_filename, i, 'test', model, i, IMG_PATCH_SIZE, PIXEL_DEPTH)
    imgpred.save(filename)
    #print(filename)
    image_filenames.append(filename)'''


#submission_filename = 'keras_submission'
#pred_to_submission(submission_filename,*image_filenames)    

with open('submission_keras.csv', 'w') as f:
        f.write('id,prediction\n')
        #for i in range(72200):
        i=0;
        for j in range(1,50+1):
          for k in range(0,593,16):
            for l in range(0,593,16): 
              strj = ''
            
              if len(str(j))<2:
                strj='00'
              elif len(str(j))==2:
                  strj='0'

              text = strj + str(j) + '_' + str(k) + '_' + str(l) + ',' + str(y_submit[i])
              f.write(text)
              f.write('\n')
              i=i+1;






