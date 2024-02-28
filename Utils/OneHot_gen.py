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
    return vocab, df

def one_hot_encode(categories, category_to_index):
    gloabl_OHV_dictionary = {}
    num_categories = len(categories)
    num_indices = len(category_to_index)
    one_hot_vectors = np.zeros((num_categories, num_indices))
    for i, category in enumerate(categories):
        index = category_to_index.get(category)
        if index is not None:
            one_hot_vectors[i, index] = 1
            gloabl_OHV_dictionary[category] = one_hot_vectors[i]
    return one_hot_vectors, gloabl_OHV_dictionary

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

def OHE_init(df):
    vocab, df = tokenize(df)
    global_one_hot_vectors, gloabl_OHV_dictionary = one_hot_encode(vocab.keys(), vocab)
    df = vectorize_and_padd(df, gloabl_OHV_dictionary)
    return df

def OHE_vector_init(df, test_size):
    df = OHE_init(df)

    x_vector = df['Lines']
    y_vector = df['Label']

    x_train, x_test, y_train, y_test = train_test_split(x_vector, y_vector, test_size=test_size)

    tensor_x_train_proto = [list([i]) for i in (x_train)]
    tensor_x_train_proto = tf.constant(tensor_x_train_proto, dtype=tf.float32)

    tensor_x_test_proto = [list([i]) for i in (x_test)]
    tensor_x_test_proto = tf.constant(tensor_x_test_proto, dtype=tf.float32)

    tensor_y_train_proto = [list([i]) for i in (y_train)]
    tensor_y_train_proto = tf.constant(tensor_y_train_proto, dtype=tf.float32)

    tensor_y_test_proto = [list([i]) for i in (y_test)]
    tensor_y_test_proto = tf.constant(tensor_y_test_proto, dtype=tf.float32)

    return tensor_x_train_proto, tensor_x_test_proto, tensor_y_train_proto, tensor_y_test_proto

