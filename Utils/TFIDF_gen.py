from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import tensorflow as tf

import platform

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

