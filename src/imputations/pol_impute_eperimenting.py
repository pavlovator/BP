import matplotlib
matplotlib.use('Qt5Agg')
import pandas as pd
import numpy as np
from sklearn.cross_validation import  train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# unnormalized data withou dates
def prepare_dataset(data, what= 'pm10'):
    x = np.array(data.iloc[:,data.columns != what])
    y = np.array(data.iloc[:,data.columns == what])
    return train_test_split(x, y, test_size=0.25)

#with time
def time_unnormalized(data):
    data = data.copy()
    data['year'] = pd.DatetimeIndex(data['dtvalue']).year
    data['month'] = pd.DatetimeIndex(data['dtvalue']).month
    data['weekday'] = pd.DatetimeIndex(data['dtvalue']).weekday + 1
    data['hour'] = pd.DatetimeIndex(data['dtvalue']).hour + 1
    return data.loc[:, data.columns != 'dtvalue']

#data and time and wind  as cirlce
def transformCycle(data, column):
    data['sin_'+column] = np.sin(2 * np.pi * data[column]/max(data[column]))
    data['cos_'+column] = np.cos(2 * np.pi * data[column]/max(data[column]))
    data.drop([column], axis=1, inplace=True)

def time_circle(data):
    data = time_unnormalized(data)
    #transformCycle(data, 'hour')
    #transformCycle(data, 'month')
    #transformCycle(data, 'weekday')
    #set not wind  (0)or variable wind (99) to (0, 0.)
    data.replace({'dd': {0: None, 99: None}}, inplace=True)
    transformCycle(data, 'dd')
    data.replace({'cos_dd': {np.NaN: 0}}, inplace=True)
    data.replace({'sin_dd': {np.NaN: 0}}, inplace=True)
    return data

#rescaled data with wind time and wind as circle



def plot_results(data ,caption):
    ks = [1,2,3,5,7,9,11,13]
    maes = []
    for k in ks:
        maes.append(modelNormal(data, k))
        print(maes[-1])
    plt.plot(ks, maes, linestyle='-', marker='o',color='red')
    plt.title(caption)
    plt.xlabel("k")
    plt.xticks(ks)
    plt.yticks(np.round(maes,2))
    plt.ylabel("MAE")
    plt.show()

def modelNormal(data1, k):
    data = data1.copy()
    scaleTarge = MinMaxScaler()
    scaleFeatures = MinMaxScaler()
    data[list(set(data.columns)-{'pm10'})] = scaleFeatures.fit_transform(data[list(set(data.columns)-{'pm10'})])
    data[['pm10']] = scaleTarge.fit_transform(data[['pm10']])
    x_train, x_test, y_train, y_test = prepare_dataset(data)
    knn = KNeighborsRegressor(n_neighbors=k, weights='distance', metric='euclidean')
    knn.fit(x_train,y_train)
    pred = knn.predict(x_test)
    pred = scaleTarge.inverse_transform(pred)
    y_test = scaleTarge.inverse_transform(y_test)
    #plt.plot(pred[1:72], color='red')
    #plt.plot(y_test[1:72], color='blue')
    #plt.show()
    return mean_absolute_error(y_test, pred)

def model(data, k):
    x_train, x_test, y_train, y_test = prepare_dataset(data)
    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(x_train,y_train)
    pred = knn.predict(x_test)
    return mean_absolute_error(y_test, pred)

data = pd.read_csv("impmeteoNonWor.csv", sep= ',')
data_cleaned = data.dropna()
#data1 = data_cleaned.loc[:, data_cleaned.columns != 'dtvalue']
data1 = time_circle(data_cleaned)
data1.drop(['no2'], axis=1, inplace= True)