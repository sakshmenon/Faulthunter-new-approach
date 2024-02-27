import numpy as np
import tensorflow as tf
import keras    

def model_init(input_shape):
    inputs = keras.Input(shape=input_shape)
    RNN_block = keras.layers.SimpleRNN(128, activation="relu")
    x = RNN_block(inputs)
    # x = keras.layers.SimpleRNN(218, activation="relu")(x)
    # x = keras.layers.SimpleRNN(128, activation="relu")(x)
    x = keras.layers.Dense(128, activation="relu")(x)
    # x = keras.layers.Dense(128, activation="relu")(x)
    # x = keras.layers.Dense(128, activation="relu")(x)
    outputs = keras.layers.Dense(1, activation="relu")(x)
    model = keras.Model(inputs = inputs, outputs = outputs, name="RNN_prototype")
    return model
