from utils import *
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import StandardScaler
from keras.optimizers import Adam
import numpy as np
from sklearn.utils import shuffle

def add_time_features(data):
    data['year'] = pd.DatetimeIndex(data['dtvalue']).year
    data['month'] = pd.DatetimeIndex(data['dtvalue']).month
    data['weekday'] = pd.DatetimeIndex(data['dtvalue']).weekday + 1
    data['hour'] = pd.DatetimeIndex(data['dtvalue']).hour + 1

def transformCycle(data, column):
    data['sin_'+column] = np.sin(2 * np.pi * data[column]/max(data[column]))
    data['cos_'+column] = np.cos(2 * np.pi * data[column]/max(data[column]))
    data.drop([column], axis=1, inplace=True)

def add_cyclic_features(dataset):
    add_time_features(dataset)
    transformCycle(dataset, 'hour')
    transformCycle(dataset, 'weekday')
    transformCycle(dataset, 'month')
    dataset.replace({'dd': {0: None, 99: None}}, inplace=True)
    transformCycle(dataset, 'dd')
    dataset.replace({'cos_dd': {np.NaN: 0}}, inplace=True)
    dataset.replace({'sin_dd': {np.NaN: 0}}, inplace=True)

def prepare_set(data, target, features):
    n_features = len(features)
    predictors = data[features]
    n_steps_out = 72
    n_steps_in = 24
    x, y = list(), list()
    for i in range(n_steps_in, len(predictors), 24):
        if i + n_steps_out > len(predictors):
            break
        x.append(predictors.loc[i - n_steps_in:i-1].values)
        y.append(predictors.loc[i:i + n_steps_out-1, target].values)
    x, y = np.array(x), np.array(y)
    x = x.reshape((x.shape[0], x.shape[1], n_features))
    return x, y

def LSTM1(x_train, y_train, x_test, y_test):
    model = Sequential()
    model.add(LSTM(200, activation='tanh',input_shape=(24, x_train.shape[2])))
    model.add(Dense(72))
    optimi = Adam(lr=0.000023)
    model.compile(optimizer=optimi, loss='mse')
    history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=50, verbose=2)
    plotHistory(history)
    return model

def scale_results(scaler, target):
    x, y = target.shape
    target = scaler.inverse_transform(target.reshape(x*y).reshape(-1,1))
    return target.reshape(x,y)

if __name__ == '__main__':
    dataset = pd.read_csv("cleaned_trnavskeknn.csv", sep=',')
    target = 'pm10'
    add_cyclic_features(dataset)
    features = ['pm10','no2','ttt','pppp','ff','sin_dd','cos_dd','sin_hour','cos_hour','sin_weekday','cos_weekday','sin_month','cos_month']
    std_scaler_features = StandardScaler().fit(dataset[features])
    std_scaler_target = StandardScaler().fit(dataset[target].values.reshape(-1,1))
    dataset[features] = std_scaler_features.transform(dataset[features])
    X, Y = prepare_set(dataset, target, features)
    x_train, y_train = X[:3653], Y[:3653]
    #x_train, y_train = shuffle(x_train,y_train)
    x_test, y_test = X[3653:], Y[3653:]
    model = LSTM1(x_train,y_train, x_test, y_test)
    y_hat = model.predict(x_test)
    y_hat = scale_results(std_scaler_target, y_hat)
    y_test = scale_results(std_scaler_target, y_test)
    e72 = errors72(y_hat, y_test)
    ploterror72(e72['mae'])
    e3 = print_score_by_days(y_hat, y_test)