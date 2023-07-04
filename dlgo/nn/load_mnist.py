import gzip
import numpy as np
import pickle

# To encode each digit from 0 to 9 so that they are represented in a 1x10 vector
# The label represents the actual digit represented in the image
def encode_label(j) -> np.ndarray:
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

# Flatten the shape of image pixels so they are represented in 1x784 vector instead of 28x28
def shape_data(data) -> iter:
    features = [np.reshape(x, (784, 1)) for x in data[0]]
    labels = [encode_label(y) for y in data[1]] # encoding the category labels into numerical representations
    return zip(features, labels)

# Load data and shape it for traininig
def load_data() -> tuple[iter, iter]:
    # TODO: get this data file
    with gzip.open('mnist.pkl.gz', 'rb') as f:
        train_data, _, test_data = pickle.load(f) # disregard validation data as it's not used here
    return shape_data(train_data), shape_data(test_data)