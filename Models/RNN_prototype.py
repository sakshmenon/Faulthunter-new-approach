import numpy as np
import tensorflow as tf
import keras    

model = keras.Sequential()

model.add(keras.layers.SimpleRNN(128))
model.add(keras.layers.SimpleRNN(128))
model.add(keras.layers.SimpleRNN(128))
model.add(keras.layers.SimpleRNN(128))
model.add(keras.layers.Dense(10))
model.add(keras.layers.Dense(10))
model.add(keras.layers.Dense(10))

model.summary()
