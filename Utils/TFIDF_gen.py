from sklearn.feature_extraction.text import TfidfVectorizer
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


def TFIDF_vectorize(x_tfidf, df):
    for vector in enumerate(x_tfidf.A):
        df['Lines'][vector[0]] = vector[1]
    return df
