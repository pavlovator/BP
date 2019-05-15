import pandas as pd
import numpy as np

def add_free_day_Col(data):
    data['weekday'] = pd.DatetimeIndex(data['dtvalue']).weekday
    data['non_working'] = np.where(data['weekday'] >= 5, 1, 0)
    del data['weekday']

data = pd.read_csv("impmeteo.csv")