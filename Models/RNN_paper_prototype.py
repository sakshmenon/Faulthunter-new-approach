import numpy as np
import tensorflow as tf
import keras    

def model_init(input_shape):
    model = keras.Sequential
    # inputs = keras.layers.Input(shape=input_shape)
    # model.add(, layer=inputs)
    model.add(keras.layers.SimpleRNN(128, activation="relu"))
    model.add(model, layer=keras.layers.Dense(128, activation="relu"))
    outputs = keras.layers.Dense(1, activation="relu")(x)

    model.add(model, layer=outputs)
    model.build(input_shape=(1,218))

    # model = keras.Model(inputs = inputs, outputs = outputs, name="RNN_prototype")
    return model
