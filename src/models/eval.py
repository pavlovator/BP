import numpy as np
from models import utils

def evalNN1(x,y,model,mms):
    preds,reals = [],[]
    for i in range(len(x)):
        scaled_prediction = model.predict(np.array([x[i]]))[0]
        unscaled_prediction = (mms.inverse_transform(scaled_prediction.reshape(-1,1))).transpose()[0]
        unscaled_real = (mms.inverse_transform(y[i].reshape(-1,1))).transpose()[0]
        preds.append(unscaled_prediction)
        reals.append(unscaled_real)
    preds, reals = np.array(preds), np.array(reals)
    preds24, preds48, preds72 = preds[:,:24], preds[:,24:48], preds[:,48:]
    reals24, reals48, reals72 = reals[:,:24], reals[:,24:48], reals[:,48:]
    print('OVERALL')
    utils.print_score(preds,reals)
    print('0-23')
    utils.print_score(preds24, reals24)
    print('24-48')
    utils.print_score(preds48, reals48)
    print('48-72')
    utils.print_score(preds72, reals72)
    return preds, reals

def evalLSTMuni(x,y,model):
    preds, reals = [], []
    for i in range(len(x)):
        prediction = model.predict(x[i].reshape((1, 24, 1)))[0]
        real = y[i]
        preds.append(prediction)
        reals.append(real)
    preds, reals = np.array(preds), np.array(reals)
    preds24, preds48, preds72 = preds[:,:24], preds[:,24:48], preds[:,48:]
    reals24, reals48, reals72 = reals[:,:24], reals[:,24:48], reals[:,48:]
    print('OVERALL')
    utils.print_score(preds,reals)
    print('0-23')
    utils.print_score(preds24, reals24)
    print('24-48')
    utils.print_score(preds48, reals48)
    print('48-72')
    utils.print_score(preds72, reals72)
    return preds, reals

def evalNN3Batch(x,y,model):
    i = 0
    arr = []
    while True:
        batch_x = x[i*24:i*24+72]
        batch_y_real = y[i*24:i*24+72].flatten()
        batch_y_hat = evalNN3_72(model,batch_x)
        i += 1
        arr.append([batch_y_real, batch_y_hat])
        if i*24+72 > len(x):
            break
    return arr


def evalNN3_72(model, x):
    y_hat72 = []
    t_1idx = 4
    for i in range(0,len(x)):
        y_1 = model.predict(np.array([x[i]]))
        y_hat72.append(y_1)
        if i +1 > len(x)-1:
            break
        x[i+1,t_1idx] = y_1
    y_hat72  = np.array(y_hat72).flatten()
    return y_hat72

