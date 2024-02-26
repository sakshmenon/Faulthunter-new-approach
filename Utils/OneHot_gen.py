import numpy as np

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

def OHV_init(df):
    vocab, df = tokenize(df)
    global_one_hot_vectors, gloabl_OHV_dictionary = one_hot_encode(vocab.keys(), vocab)
    df = vectorize_and_padd(df, gloabl_OHV_dictionary)
    return df