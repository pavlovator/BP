import matplotlib
matplotlib.use('Qt5Agg')
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def time_unnormalized(data):
    data = data.copy()
    data['year'] = pd.DatetimeIndex(data['dtvalue']).year
    data['month'] = pd.DatetimeIndex(data['dtvalue']).month
    data['weekday'] = pd.DatetimeIndex(data['dtvalue']).weekday + 1
    data['hour'] = pd.DatetimeIndex(data['dtvalue']).hour + 1
    return data.loc[:, data.columns != 'dtvalue']

def transformCycle(data, column):
    data['sin_'+column] = np.sin(2 * np.pi * data[column]/max(data[column]))
    data['cos_'+column] = np.cos(2 * np.pi * data[column]/max(data[column]))
    data.drop([column], axis=1, inplace=True)

def prepare_model(data1,what,drop=False):
    data = data1.copy()
    data.dropna(inplace = True)
    if drop != False:
        data.drop([drop], axis = 1, inplace= True)
    data = time_unnormalized(data)
    data.replace({'dd': {0: None, 99: None}}, inplace=True)
    transformCycle(data, 'dd')
    data.replace({'cos_dd': {np.NaN: 0}}, inplace=True)
    data.replace({'sin_dd': {np.NaN: 0}}, inplace=True)


    scaleTarge = MinMaxScaler()
    scaleFeatures = MinMaxScaler()
    x = np.array(data.iloc[:, data.columns != what])
    y = np.array(data.iloc[:, data.columns == what])
    x = scaleFeatures.fit_transform(x)
    y = scaleTarge.fit_transform(y)

    knn = KNeighborsRegressor(n_neighbors=2, weights='distance', metric='euclidean')
    knn.fit(x, y)
    return knn, scaleTarge, scaleFeatures



def make_features(row):
    dd = row['dd']
    if dd == 0 or dd == 99:
        cos_dd, sin_dd = 0, 0
    else:
        sin_dd = np.sin(2 * np.pi * dd / 36)
        cos_dd = np.cos(2 * np.pi * dd / 36)
    features = []
    date = pd.Timestamp(row['dtvalue'])
    features+= [row['ttt'], row['td'],row['ff'], row['pppp'], row['pm10'], row['non_working'], date.year, date.month, date.weekday() +1, date.hour +1, sin_dd, cos_dd]
    return features

def make_features2(row):
    dd = row['dd']
    if dd == 0 or dd == 99:
        cos_dd, sin_dd = 0, 0
    else:
        sin_dd = np.sin(2 * np.pi * dd / 36)
        cos_dd = np.cos(2 * np.pi * dd / 36)
    features = []
    date = pd.Timestamp(row['dtvalue'])
    features+= [row['no2'],row['ttt'], row['td'],row['ff'], row['pppp'], row['non_working'], date.year, date.month, date.weekday() +1, date.hour +1, sin_dd, cos_dd]
    return features

def make_features3(row):
    dd = row['dd']
    if dd == 0 or dd == 99:
        cos_dd, sin_dd = 0, 0
    else:
        sin_dd = np.sin(2 * np.pi * dd / 36)
        cos_dd = np.cos(2 * np.pi * dd / 36)
    features = []
    date = pd.Timestamp(row['dtvalue'])
    features+= [row['ttt'], row['td'],row['ff'], row['pppp'], row['non_working'], date.year, date.month, date.weekday() +1, date.hour +1, sin_dd, cos_dd]
    return features



def knn_imputeNO2(data, model, scalerT, scalerF):
    for i, row in data.iterrows():
        if np.isnan(row['no2']) and not np.isnan(row['pm10']):
            predictors = make_features(row)
            value = model.predict(scalerF.transform([predictors]))
            value = scalerT.inverse_transform(value)
            data.loc[i, 'no2'] = value[0][0]

def knn_imputePM10(data, model, scalerT, scalerF):
    for i, row in data.iterrows():
        if np.isnan(row['pm10']) and not np.isnan(row['no2']):
            predictors = make_features2(row)
            value = model.predict(scalerF.transform([predictors]))
            value = scalerT.inverse_transform(value)
            data.loc[i, 'pm10'] = value[0][0]

def knn_imputePM10withoutNO2(data, model, scalerT, scalerF):
    for i, row in data.iterrows():
        if np.isnan(row['pm10']):
            predictors = make_features3(row)
            value = model.predict(scalerF.transform([predictors]))
            value = scalerT.inverse_transform(value)
            data.loc[i, 'pm10'] = value[0][0]

def knn_imputeNo2withoutPM10(data,model, scalerT, scalerF):
    for i, row in data.iterrows():
        if np.isnan(row['no2']):
            predictors = make_features3(row)
            value = model.predict(scalerF.transform([predictors]))
            value = scalerT.inverse_transform(value)
            data.loc[i, 'no2'] = value[0][0]


data = pd.read_csv("no2pm10pm10imp.csv", sep= ',')
print(len(data['no2']) - data['no2'].count())

model, scalerT, scalerF = prepare_model(data, 'no2','pm10')