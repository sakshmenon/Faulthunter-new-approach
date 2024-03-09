import tensorflow as tf
import string
import re
import platform
import os
import numpy as np
from sklearn.model_selection import train_test_split


vocab_size = 4096
SEED = 42
AUTOTUNE = tf.data.AUTOTUNE

def path_changes(gpu_token):
    if platform.machine() == 'arm64':
        pth = "/Users/saksh.menon/Documents/GitHub/C-RNN-approach/Labels"
    elif platform.machine() == 'x86_64':
        if gpu_token:
            pth = "/home/ucdasec/Faulthunter-RNN-approach/Labels"
        else:
            pth = "/home/sakshmeno/Documents/GitHub/C-RNN-approach/Labels"

    return pth

def pad_init(df):
    max_len = 0
    for i in range(df.shape[0]):
        if  len(df['Lines'][i]) > max_len:
            max_len = (len(df['Lines'][i]))
    return max_len


def filtered_gen(df):
    codeLines = list(df['Lines'])
    with open('FILTERED_CODE.txt', 'w') as fc_obj:
        # fc_obj.writelines(codeLines)
        for i in range(len(codeLines)):
            fc_obj.writelines(codeLines[i])
            fc_obj.write('\n')

def word2vec_init(df, gpu_token):  
    pth = path_changes(gpu_token) 
    os.chdir(pth) 
    filtered_gen(df)
    # os.chdir(pth)
    text_ds = tf.data.TextLineDataset(pth + "/FILTERED_CODE.txt").filter(lambda x: tf.cast(tf.strings.length(x), bool))

    def custom_standardization(input_data):
        lowercase = tf.strings.lower(input_data)

        return tf.strings.regex_replace(lowercase,
                                        '[%s]' % re.escape(string.punctuation), '')
    sequence_length = pad_init(df)
    vectorize_layer = tf.keras.layers.TextVectorization(
        standardize=custom_standardization,
        max_tokens=vocab_size,
        output_mode='int',
        output_sequence_length=sequence_length)

    vectorize_layer.adapt(text_ds.batch(1024))

    text_vector_ds = text_ds.batch(1024).prefetch(AUTOTUNE).map(vectorize_layer).unbatch()
    sequences = list(text_vector_ds.as_numpy_iterator())
    inverse_vocab = vectorize_layer.get_vocabulary()

    for vector in enumerate(sequences):
        df['Encoded Lines'][vector[0]] = np.array(vector[1]).astype(dtype="float32")
        
    return df
