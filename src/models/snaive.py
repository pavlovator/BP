from utils import *
import pandas as pd
import numpy as np

def snaive(dset, h):
    y_hat = []
    y_real = []
    for i in range(h,len(dset),24):
        if i +72 > len(dset):
            break
        y_real.append(dset[i:i+72])
        y_hat.append(dset[i-h:i-h+72])
    return np.array(y_hat), np.array(y_real)

if __name__ == '__main__':
    dataset = pd.read_csv("cleaned_trnavskeknn.csv", sep=',')
    series = np.array(dataset['pm10'])
    test_set = series[87672-6*24:] #od zaciatku roka 2013
    y_hat, y_real = snaive(test_set,7*24)
    errors = errors72(y_hat, y_real)
    ploterror72(errors['mae'])
    dayserror = print_score_by_days(y_hat, y_real)