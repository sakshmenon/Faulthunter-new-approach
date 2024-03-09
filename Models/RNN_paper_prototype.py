import numpy as np
import tensorflow as tf
import keras    
from keras import layers

def model_init(input_shape):
    model = keras.Sequential()

    model.add(layers.Input((input_shape, 1)))
    model.add(layers.SimpleRNN(1024, return_sequences=True, dropout=0.4))
    model.add(layers.SimpleRNN(1024, return_sequences=True, dropout=0.4))
    model.add(layers.SimpleRNN(1024, dropout=0.4))
    model.add(layers.Dense(1024, activation=keras.activations.relu)) #kernel_regularizer=keras.regularizers.l2(0.01)
    model.add(layers.Dense(1024, activation=keras.activations.relu ))
    model.add(layers.Dense(1024, activation=keras.activations.relu ))
    model.add(layers.Dense(2, activation = keras.activations.softmax))

    model.compile(optimizer=keras.optimizers.legacy.Adam(learning_rate=0.0001), loss=keras.losses.BinaryFocalCrossentropy(apply_class_balancing=True,gamma=2),
                metrics=["accuracy"], )
    return model
