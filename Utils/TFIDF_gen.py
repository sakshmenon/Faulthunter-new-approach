from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import tensorflow as tf

import platform
# import dataframe_gen

if platform.machine() == 'arm64':
    pth = "/Users/saksh.menon/Documents/GitHub/C-RNN-approach/Labels/DATASET.txt"
elif platform.machine() == 'x86_64':
    pth = "/home/sakshmeno/Documents/GitHub/C-RNN-approach/Labels/DATASET.txt"

def line_gen(df):
    codeLines = list(df['Lines'])
    vectorizer = TfidfVectorizer()
    transformed_output = vectorizer.fit_transform(codeLines)
    all_feature_names = vectorizer.get_feature_names_out()
    x_tfidf = vectorizer.fit_transform(df['Lines'])
    return x_tfidf


def TFIDF_init(df):
    x_tfidf = line_gen(df)
    for vector in enumerate(x_tfidf.A):
        df['Lines'][vector[0]] = vector[1]
    return df

def TFIDF_vector_init(df, test_size):
    df = TFIDF_init(df)

    x_vector = df['Lines']
    y_vector = df['Label']

    x_train, x_test, y_train, y_test = train_test_split(x_vector, y_vector, test_size)

    tensor_x_train_proto = [list([i]) for i in (x_train)]
    tensor_x_train_proto = tf.constant(tensor_x_train_proto, dtype=tf.float32)

    tensor_x_test_proto = [list([i]) for i in (x_test)]
    tensor_x_test_proto = tf.constant(tensor_x_test_proto, dtype=tf.float32)

    tensor_y_train_proto = [list([i]) for i in (y_train)]
    tensor_y_train_proto = tf.constant(tensor_y_train_proto, dtype=tf.float32)

    tensor_y_test_proto = [list([i]) for i in (y_test)]
    tensor_y_test_proto = tf.constant(tensor_y_test_proto, dtype=tf.float32)

    return tensor_x_train_proto, tensor_x_test_proto, tensor_y_train_proto, tensor_y_test_proto

