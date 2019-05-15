import pandas as pd
import numpy as np
data = pd.read_csv("trnavskemyto.csv", sep = ',')

def coverage(data):
    data['dtvalue'] = pd.to_datetime(data['dtvalue'])
    by_year = data.groupby(data['dtvalue'].dt.year).apply(lambda x: x.notnull().mean() * 100)
    del by_year['dtvalue']
    return by_year

#inplace imputations

def imputateOnNeighbours(data):
    cols = list(set(data.columns) - {'dtvalue', 'pm10', 'no2'})
    k = 0
    overall = 0
    for col in cols:
        k = 0
        for i in range(1, len(data)-1):
            if np.isnan(data.loc[i,col]) and not np.isnan(data.loc[i-1, col]) and not np.isnan(data.loc[i+1, col]):
                k += 1
                if col == 'dd':
                    data.loc[i, col] = data.loc[i-1, col]
                elif col == 'ff':
                    data.loc[i, col] = data.loc[i-1, col]
                else:
                    data.loc[i, col] = (data.loc[i-1, col] + data.loc[i+1, col])/2
        overall += k
        #print(col, k)
    print("Imputations on Neigh: {:}".format(overall))

def imputate2010Gap(data):
    missstart = 63823
    missend = 64533
    imputestart = 55063
    cols = list(set(data.columns) - {'dtvalue', 'pm10', 'no2'})
    for i in range(0, missend-missstart):
        for col in cols:
            data.loc[missstart+i, col] = data.loc[imputestart+i, col]
    print("Imputations on 2010 Gap")





def imputateDailySeason(data):
    print("Imputation on last day")
    cols = list(set(data.columns) - {'dtvalue', 'pm10', 'no2'})
    k = 0
    overall = 0
    for col in cols:
        k = 0
        for i in range(1, len(data) - 1):
            if np.isnan(data.loc[i, col]) and not np.isnan(data.loc[i - 24, col]):
                k += 1
                data.loc[i, col] = data.loc[i - 24, col]
        overall += k
        #print(col, k)
    print("Imputations on Daily Season: {:}".format(overall))

def imputateAllMeteo(data):
    imputateOnNeighbours(data)
    #last observed one step
    data.interpolate(method='nearest', limit=1, inplace=True) #toto robi aj no2 a pm10
    imputateOnNeighbours(data)
    imputate2010Gap(data)
    imputateDailySeason(data)


