import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


def create_model(x_train, y_train, layers, dim, epochs=1000):
    np.random.seed(7)    
    x = np.array(x_train)
    y = np.array(y_train)

    model = Sequential()
    model.add(Dense(layers[0], input_dim=dim, activation='relu'))
    for i in range(1, len(layers)-1):
        model.add(Dense(layers[i], activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    model.fit(x, y, epochs=epochs, verbose=2)
    return model

