# -*- coding: utf-8 -*-
"""Automated_Seismic_Phase_Recognition_Using_Neural_Networks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RjDUzEEvewUzNJ-6q7h2bHTf-0ViXKO1

# *Automated Seismic Phase Recognition Using Neural Networks*
##### Syed Ali Raza Rizvi
"""

# Downloading the file using the wget tool
# The file is quite large at 21 Gb, so a hosted runtime is probably better than a local one.
# If you are using Google Colaboratory, try and connect to a TPU (Tensor-Processing-Unit) Runtime, since it will have the necessary RAM and storage requirements.
!wget "https://service.scedc.caltech.edu/ftp/ross_etal_2018_bssa/scsn_ps_2000_2017_shuf.hdf5"

# Importing the necessary libraries
import tensorflow as tf
import numpy as np
import matplotlib as mpt
import matplotlib.pyplot as plt
import keras
import h5py

# Defining the data with the name 'dataset'
dataset = h5py.File("/content/scsn_ps_2000_2017_shuf.hdf5", 'r')

# X_signal is the dataset with the data streams
# X_signal contains 4773750 seismic waveforms, with each waveform having 3 (X, Y, Z axis) and being a list 400 floats long (due to 100 hz for 4 seconds)
X_signal=dataset['X']
# Y_classification contains the label for the corresponding X_test value: 0 = Seismic Noise, 1 = P wave, 2 = S wave
Y_classification=dataset['Y']
print(X_signal)
print(Y_classification)

print(X_signal[0])
print(Y_classification[0])

# Printing example X, Y, and Z axis seismograms for seismic noise

stream_1=[]
stream_2=[]
stream_3=[]

for i in X_signal[0]:
  stream_1.append(i[0])
  stream_2.append(i[1])
  stream_3.append(i[2])
unified=[stream_1, stream_2, stream_3]

font = {'family': "DejaVu Sans",
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }


for i in unified:
  X = np.arange(len(i)) 
  plt.figure(figsize=(15,5))
  plt.plot(X, i, color='#ab802b')
  plt.xlabel('Time (sec)', fontdict=font)
  plt.ylabel('Ground Velocity (m/sec)',  fontdict=font)
  plt.title('Seismic Noise',  fontdict=font)
  plt.gca().tick_params(axis='both', direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
  plt.show()

# Printing example X, Y, and Z axis seismograms for a P wave

stream_1=[]
stream_2=[]
stream_3=[]

for i in X_signal[1]:
  stream_1.append(i[0])
  stream_2.append(i[1])
  stream_3.append(i[2])
unified=[stream_1, stream_2, stream_3]

font = {'family': "DejaVu Sans",
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }


for i in unified:
  X = np.arange(len(i)) 
  plt.figure(figsize=(15,5))
  plt.plot(X, i, color='#ab802b')
  plt.xlabel('Time (sec)', fontdict=font)
  plt.ylabel('Ground Velocity (m/sec)',  fontdict=font)
  plt.title('P Waves',  fontdict=font)
  plt.gca().tick_params(axis='both', direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
  plt.show()

# Printing example X, Y, and Z axis seismograms for an S Wave

stream_1=[]
stream_2=[]
stream_3=[]

for i in X_signal[2]:
  stream_1.append(i[0])
  stream_2.append(i[1])
  stream_3.append(i[2])
unified=[stream_1, stream_2, stream_3]

font = {'family': "DejaVu Sans",
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }


for i in unified:
  X = np.arange(len(i)) 
  plt.figure(figsize=(15,5))
  plt.plot(X, i, color='#ab802b')
  plt.xlabel('Time (sec)', fontdict=font)
  plt.ylabel('Ground Velocity (m/sec)',  fontdict=font)
  plt.title('S Waves',  fontdict=font)
  plt.gca().tick_params(axis='both', direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
  plt.show()

# Extracting the first 10% of the data due to RAM usage restrictions in Colab and re-arranging it in a numpy array
# Also splitting data into training and testing data with a 80:20 split

extracted_data=int((0.1*len(X_signal)))

X_train=[]
for i in X_signal[0:int(0.8*extracted_data)]:
    trace_1=[]
    trace_2=[]
    trace_3=[]
    for g in i:
        trace_1.append(g[0])
        trace_2.append(g[1])
        trace_3.append(g[2])
    X_train.append([trace_1, trace_2, trace_3])

X_test=[]
for i in X_signal[int(0.8*extracted_data):extracted_data]:
    trace_1=[]
    trace_2=[]
    trace_3=[]
    for g in i:
        trace_1.append(g[0])
        trace_2.append(g[1])
        trace_3.append(g[2])
    X_test.append([trace_1, trace_2, trace_3])

Y_train = Y_classification[0:int(0.8*extracted_data)]
Y_test = Y_classification[int(0.8*extracted_data):extracted_data]

# Flipping the rows and columns of the dataset to make it easier for the machine learning model to interpret
# Changing the nested lists to a numpy arrray 

X_train_final=[]
X_test_final=[]

for i in X_train:
    X_train_final.append(np.array(i))

for i in X_test:
    X_test_final.append(np.array(i))


X_train_final=np.array(X_train_final)
X_test_final=np.array(X_test_final)

# One hot encoding the labels for the sequence classifier
from keras.utils import to_categorical

Y_train=to_categorical(Y_train)
Y_test=to_categorical(Y_test)

# Create a model using the Keras Sequential API

from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Flatten, Conv1D
from keras.callbacks import EarlyStopping, ModelCheckpoint


model = Sequential()
model.add(Conv1D(200, 2, activation='relu'))
model.add(Conv1D(130, 2, activation='relu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(200, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dense(150, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
classifier=model.fit(
    X_train_final, Y_train, batch_size=100, epochs=50, validation_data=(X_test_final, Y_test), 
    callbacks=[EarlyStopping(monitor='val_loss', patience=3), ModelCheckpoint(filepath='Best_Model.hdf5', save_best_only=True)]
    )
print(model.summary())

# Generating an Accuracy vs Epoch graph

font = {'family': "DejaVu Sans",
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }

plt.plot(classifier.history['acc'], color='red')
plt.plot(classifier.history['val_acc'], color= 'blue')
plt.xlabel('Epoch', fontdict=font)
plt.ylabel('Accuracy', fontdict=font)
plt.title('Model Accuracy', fontdict=font)
plt.legend(['Train', 'Test'], loc='lower right')
plt.gca().tick_params(axis='both', direction='out', length=6, width=2, colors='black', grid_alpha=0.5)
plt.show()

# Generating a Loss vs Epoch graph

font = {'family': "DejaVu Sans",
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }

plt.plot(classifier.history['loss'], color='red')
plt.plot(classifier.history['val_loss'], color='blue')
plt.xlabel('Epoch', fontdict=font)
plt.ylabel('Loss', fontdict=font)
plt.title('Model Loss', fontdict=font)
plt.legend(['Train', 'Test'], loc='lower right')
plt.gca().tick_params(axis='both', direction='out', length=6, width=2, colors='black', grid_alpha=0.5)
plt.show()