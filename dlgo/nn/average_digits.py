import numpy as np
from dlgo.nn.load_mnist import load_data

# 
def average_digit(data, digit) -> float:
    filtered_data = [x[0] for x in data if np.argmax(x[1])==digit]
    filtered_array = np.asarray(filtered_data)
    return np.average(filtered_array, axis=0)

train, test = load_data()
avg_eight = average_digit(train, 8)