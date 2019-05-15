import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from numpy import sqrt
import numpy as np
from scipy.stats.stats import pearsonr
import json


def compare(y,y_hat):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    major_ticks = np.arange(0, 73, 24)
    minor_ticks = np.arange(0, 73, 1)
    xsteps = list(range(72))
    ax.plot(xsteps, y, '.-', color='r')
    ax.plot(xsteps, y_hat, '.-', color='b')
    ax.legend(('real', 'forecast'), loc='upper right')
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.grid(which='major', alpha=0.5)
    plt.show()

def errors72(yhat,y):
    rmse,mae,mb, mfb, mfe, r = [],[],[],[],[],[]
    for i in range(72):
        rmse.append(sqrt(mean_squared_error(y[:,i], yhat[:,i])))
        mae.append(mean_absolute_error(y[:,i], yhat[:,i]))
        mb.append(MB(yhat[:,i].reshape(-1,1), y[:,i].reshape(-1,1)))
        mfb.append(MFB(yhat[:,i].reshape(-1,1), y[:,i].reshape(-1,1)))
        mfe.append(MFE(yhat[:,i].reshape(-1,1),y[:,i].reshape(-1,1)))
        r.append(correlation(yhat[:,i].reshape(-1,1),y[:,i].reshape(-1,1))[0])
    return {"rmse":rmse, 'mae':mae,'mb':mb,"mfb":mfb, 'mfe':mfe,'r':r}

def ploterror72(error):
    plt.figure(2)
    plt.plot(list(range(72)), error , '.-', color='b')
    plt.show()

def plotHistory(history):
    plt.figure(1)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.xticks(list(range(0,len(history.epoch),len(history.epoch)//10)))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()


def print_score_by_days(preds,reals):
    preds24, preds48, preds72 = preds[:, :24], preds[:, 24:48], preds[:, 48:]
    reals24, reals48, reals72 = reals[:, :24], reals[:, 24:48], reals[:, 48:]
    print('OVERALL')
    overall = print_score(preds, reals)
    print('0-23')
    day1 = print_score(preds24, reals24)
    print('24-48')
    day2 = print_score(preds48, reals48)
    print('48-72')
    day3 = print_score(preds72, reals72)
    return {"overall": overall,"day1":day1, "day2":day2, "day3":day3}


def MB(y_hat, y):
    return np.mean(sum(y_hat - y)/len(y))

def MFB2(y_hat, y):
    vysl = 0
    for riadok in range(len(y)):
        for stlpec in range(len(y[0])):
            m,o = y_hat[riadok, stlpec] , y[riadok, stlpec]
            vysl += (m-o)/((o+m)/2)
    vysl = vysl / (len(y[0]) * len(y))
    return vysl

def MFB(y_hat, y):
    return np.mean(sum((y_hat - y) / ((y+y_hat)/2))/len(y))*100

def MFE2(y_hat, y):
    vysl = 0
    for riadok in range(len(y)):
        for stlpec in range(len(y[0])):
            m, o = y_hat[riadok, stlpec] , y[riadok, stlpec]
            vysl += np.abs(m - o) / ((o + m) / 2)
    vysl = vysl / (len(y[0]) * len(y))
    return vysl

def MFE(y_hat, y):
    return np.mean(sum(abs(y_hat - y) / ((y + y_hat) / 2)) / len(y))*100

def correlation(y_hat, y):
    return pearsonr(y_hat.flatten(),y.flatten())

def print_score(y,y_hat):
    rmse, mae, mb, mfb, mfe, r = sqrt(mean_squared_error(y, y_hat)), mean_absolute_error(y, y_hat), MB(y_hat,y),MFB(y_hat,y),MFE(y_hat,y),correlation(y_hat,y)[0]
    print("RMSE: {:}".format(rmse))
    print("MAE: {:}".format(mae))
    print("MB: {:}".format(mb))
    print("MFB: {:}".format(mfb))
    print("MFE: {:}".format(mfe))
    print("r: {:}".format(r))
    return {"rmse":np.round(rmse,2), 'mae':np.round(mae,2),'mb':np.round(mb,2),"mfb":np.round(mfb,2), 'mfe':np.round(mfe,2),'r':np.round(r,2)}

def save_dict(data, name):
    with open(name, 'w') as fp:
        json.dump(data, fp, indent=4)