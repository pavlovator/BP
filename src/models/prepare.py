import pandas as pd
import numpy as np

def prepareNN1(data, pol,scaler,n_steps_in=24):
    '''
    UNI MLP
    :param n_steps_in:
    :param n_steps_out:
    :return: dataset for simple univariate multilayer perceptron input 24 lagged values of pollutant output 72 step forecast
    '''
    series = data[pol]
    series = np.array(series)
    n_steps_out = 72
    x, y = list(), list()
    for i in range(n_steps_in, len(series),24):
        if i + n_steps_out > len(series):
            break
        x.append(scaler.transform((series[i - n_steps_in:i]).reshape(-1,1)).transpose()[0])
        y.append(scaler.transform((series[i :i + n_steps_out]).reshape(-1,1)).transpose()[0])
    return np.array(x), np.array(y)


def prepareNN2(data, pol, n_steps_in=24):
    '''
    MULTI MLP
    :param data:
    :param pol:
    :param n_steps_in:
    :return: dataset for multivariate multilayer perceptron input 24 * |cols| lagged values output 72 step forecast
    '''
    cols = ['ttt','td','dd','ff','pppp','pm10']
    multiseries = data[cols].values
    series = np.array(data[pol])
    n_steps_out = 72
    x, y = list(), list()
    for i in range(n_steps_in, len(multiseries),24):
        if i + n_steps_out > len(multiseries):
            break
        x.append(np.concatenate(multiseries[i - n_steps_in:i]))
        y.append(series[i :i + n_steps_out])
    return np.array(x), np.array(y)

def prepareNN3(data1,pol,scaler):
    '''
    :param data1:
    :param pol:
    :return: dataset for recursive approach for NN
    '''
    data = data1.copy()
    data['month'] = pd.DatetimeIndex(data['dtvalue']).month
    data['weekday'] = pd.DatetimeIndex(data['dtvalue']).weekday + 1
    data['hour'] = pd.DatetimeIndex(data['dtvalue']).hour + 1
    transformCycle(data,'month')
    transformCycle(data,'weekday')
    transformCycle(data,'hour')
    multiseries_in = data[['cos_month','sin_month','sin_weekday','cos_weekday','cos_hour','sin_hour','non_working']].values
    series_out = np.array(data[pol])
    n_steps_out = 1
    x, y = list(), list()
    for i in range(1, len(multiseries_in),1):
        if i + n_steps_out > len(multiseries_in):
            break
        inp_features = multiseries_in[i]
        inp_features = np.append(inp_features,scaler.transform(series_out[i-1])[0,0])
        x.append(inp_features)
        y.append(scaler.transform(series_out[i])[0,0])
    return np.array(x), np.array(y)

def transformCycle(data, column):
    data['sin_'+column] = np.sin(2 * np.pi * data[column]/max(data[column]))
    data['cos_'+column] = np.cos(2 * np.pi * data[column]/max(data[column]))
    data.drop([column], axis=1, inplace=True)



DATASET = pd.read_csv("cleaned_trnavskeknn.csv",sep=',')
DATASETPO2013 = DATASET.loc[0:87671,:]
DATASETOD2013 = DATASET.loc[87672:,:]
DATASETOD2013.reset_index(drop=True, inplace=True)