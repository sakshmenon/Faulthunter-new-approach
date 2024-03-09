from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import numpy as np

def vec_split(df):
    secure_vector = []
    insecure_vector = []

    for label in enumerate(df['Label']):
        if label[1] == [0,1]:
            insecure_vector.append(df.loc[label[0]])
        else:
            secure_vector.append(df.loc[label[0]])

    secure_df = pd.DataFrame(secure_vector)
    insecure_df = pd.DataFrame(insecure_vector)

    x_train_secure, x_test_secure, y_train_secure, y_test_secure = train_test_split(secure_df['Lines'], secure_df['Label'], random_state=32, test_size = 0.2)
    x_train_insecure, x_test_insecure, y_train_insecure, y_test_insecure = train_test_split(insecure_df['Lines'], insecure_df['Label'], random_state=32, test_size = 0.2)

    #80%
    training_df = pd.DataFrame({'Lines':x_train_secure,'Label':y_train_secure})
    rand_idx = np.random.randint(0, len(training_df), size=len(x_train_insecure))
    for i in enumerate(rand_idx):
        new_row = pd.DataFrame({'Lines':[list(x_train_insecure)[i[0]]],'Label':[list(y_train_insecure)[i[0]]]})
        training_df = pd.concat([training_df.iloc[:i[1]], new_row, training_df.iloc[i[1]:]], ignore_index=True)

    testing_df = pd.DataFrame({'Lines':x_test_secure,'Label':y_test_secure})
    rand_idx = np.random.randint(0, len(testing_df), size=len(x_test_insecure))
    for i in enumerate(rand_idx):
        new_row = pd.DataFrame({'Lines':[list(x_test_insecure)[i[0]]],'Label':[list(y_test_insecure)[i[0]]]})
        testing_df = pd.concat([testing_df.iloc[:i[1]], new_row, testing_df.iloc[i[1]:]], ignore_index=True)

    training_df['Encoded Lines'] = training_df['Lines']
    testing_df['Encoded Lines'] = testing_df['Lines']

    return training_df, testing_df

def tensor_gen(vectors):

    # vectors[0]['Tensors'] = vectors[0]['Encoded Lines']
    # vectors[1]['Tensors'] = vectors[1]['Encoded Lines']


    x_train = vectors[0]['Encoded Lines']
    x_test = vectors[1]['Encoded Lines']
    y_train = vectors[0]['Label']
    y_test = vectors[1]['Label']

    tensor_x_train_proto = [i for i in (x_train)]
    tensor_x_train_proto = tf.constant(tensor_x_train_proto, dtype=tf.float32)

    # vectors[0]['Tensors'] = tensor_x_train_proto

    tensor_x_test_proto = [i for i in (x_test)]
    tensor_x_test_proto = tf.constant(tensor_x_test_proto, dtype=tf.float32)

    # vectors[1]['Tensors'] = tensor_x_test_proto

    tensor_y_train_proto = [i for i in (y_train)]
    tensor_y_train_proto = tf.constant(tensor_y_train_proto, dtype=tf.float32)

    tensor_y_test_proto = [i for i in (y_test)]
    tensor_y_test_proto = tf.constant(tensor_y_test_proto, dtype=tf.float32)
        
    return tensor_x_train_proto, tensor_x_test_proto, tensor_y_train_proto, tensor_y_test_proto
