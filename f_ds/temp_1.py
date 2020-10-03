from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
import numpy as np 

def get_model_proba(train, res, layers, digits):
    x = np.array(train)
    y = np.array(res)
    model = Sequential()
    model.add(Dense(layers[0], input_dim=digits, activation='tanh'))
    for i in range(1, len(layers)-1):
        model.add(Dense(layers[i], activation='tanh'))
    model.add(Dense(1, activation='sigmoid'))

    sgd = SGD(lr=0.1)
    model.compile(loss='binary_crossentropy', optimizer=sgd)

    model.fit(x, y, batch_size=1, nb_epoch=1000, verbose=2)
    return model

def to_bit_list(num, digits):
    s = '{0:b}'.format(num).zfill(digits)
    return [int(x) for x in list(s)]

digits = 8
train = list()
res = list()
for i in range(200):
    train.append(to_bit_list(i,digits))
    if i < 100:
        res.append(0)
    else:
        res.append(1)

#train = [[0, 0], [0, 1], [1, 0], [1, 1]]
#res = [[0], [1], [1], [0]]

train = [[1,1],[1,1],[1,1],[1,1],[1,0],[0,1],[0,0],[0,0],[0,0],[0,0]]
res = [[1],[1],[1],[1],[1],[0],[0],[0],[0],[0]]
model = get_model_proba(train, res, [8], 2)

y_pred = model.predict_proba(np.array([[0,1]]))
print(y_pred)