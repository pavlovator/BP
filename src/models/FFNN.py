from utils import *
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
def prepare_set(series):
    series = np.array(series)
    n_steps_out = 72
    n_steps_in = 24
    x, y = list(), list()
    for i in range(n_steps_in, len(series), 24):
        if i + n_steps_out > len(series):
            break
        x.append(series[i - n_steps_in:i])
        y.append(series[i:i + n_steps_out])
    return np.array(x), np.array(y)


def FFNN(x_train, y_train, x_test, y_test):
    model = Sequential()
    model.add(Dense(150, activation='relu', input_dim=24))
    model.add(Dropout(0.2))
    model.add(Dense(72))
    optimizer = Adam(lr=0.0005)
    model.compile(optimizer=optimizer, loss='mse')
    history = model.fit(x_train, y_train, batch_size=32, validation_data = (x_test, y_test), epochs=100, verbose=2)
    plotHistory(history)
    return model





if __name__ == '__main__':
    dataset = pd.read_csv("cleaned_trnavskeknn.csv", sep=',')
    series = dataset['no2']
    train_set = series[:87671] #po koniec roka 2013
    test_set = series[87672:] #od zaciatku roka 2013
    x_train, y_train = prepare_set(train_set)
    x_test, y_test = prepare_set(test_set)
    model = FFNN(x_train, y_train, x_test, y_test)
    y_hat = model.predict(x_test)
    chyby72 = errors72(y_hat, y_test)
    ploterror72(chyby72['mae'])
    daylyerror = print_score_by_days(y_hat, y_test)
