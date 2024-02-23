import dataframe_gen
import numpy as np

df = dataframe_gen.dataframe_init()

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

global_one_hot_vectors, gloabl_OHV_dictionary = one_hot_encode(vocab.keys(), vocab)

for line in range(df.shape[0]):
    df.loc[line].Lines = df.loc[line].Lines.split()
    for element_index in range(len(df.loc[line].Lines)):
        df.loc[line].Lines[element_index] = gloabl_OHV_dictionary[df.loc[line].Lines[element_index]]

max_len = 0
for i in range(df.shape[0]):
    if  len(df.loc[i].Lines) > max_len:
        max_len = (len(df.loc[i].Lines))
for i in enumerate(df.loc[:]):
    for iter in range(0, max_len - len(i[1])):
        df.loc[i[0]].Lines.insert(-1, gloabl_OHV_dictionary['<pad>'])