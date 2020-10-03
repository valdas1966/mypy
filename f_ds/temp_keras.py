from keras.models import Sequential
from keras.layers import Dense
import numpy as np



def get_model_proba(train, res, layers, epochs=1000):
    np.random.seed(7)    
    x = np.array(train)
    y = np.array(res)

    model = Sequential()
    model.add(Dense(layers[0], input_dim=4, activation='relu'))
    for i in range(1,len(layers)-1):
        model.add(Dense(layers[i], activation='relu'))
    model.add(Dense(4, activation='softmax'))
    #model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.fit(x, y, epochs=epochs, verbose=2)
    return model


                
    model = get_model_proba(train, res, [4,8,16,64,4],1000)
    
    
def to_binary_list(num, digits):
    s = '{0:b}'.format(num).zfill(digits)
    return [int(x) for x in list(s)]
    

for i in range(16):
    print(i, to_binary_list)