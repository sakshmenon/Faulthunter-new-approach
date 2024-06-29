import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

def tokenize(df):

    x_vec = df['Lines']
    y_vec = df['Label']

    vocab, index = {}, 1  # start indexing from 1
    vocab['<pad>'] = 0  # add a padding token

    for line in np.asarray(x_vec):
        tokens = list(line.split())
        for token in tokens:
            if token not in vocab:
                vocab[token] = index
                index += 1
    return vocab

def vectorize_and_padd(df, gloabl_OHV_dictionary):
    for line in range(df.shape[0]):
        df['Lines'][line] = df['Lines'][line].split()
        for element_index in range(len(df['Lines'][line])):
            df['Lines'][line][element_index] = gloabl_OHV_dictionary[df['Lines'][line][element_index]]

    max_len = 0
    for i in range(df.shape[0]):
        if  len(df['Lines'][i]) > max_len:
            max_len = (len(df['Lines'][i]))
    for i in enumerate(df['Lines']):
        for iter in range(0, max_len - len(i[1])):
            df['Lines'][i[0]].append(gloabl_OHV_dictionary['<pad>'])
        df['Lines'][i[0]] = np.array(df['Lines'][i[0]])
    return df

def word2vec_ver2_init(vectors, original_df):
    vocab = tokenize(original_df)
    for vector in vectors:
        for i in enumerate(vector['Lines']):
            vector['Encoded Lines'][i[0]] = [vocab[j] for j in i[1].split()]
    return vectors