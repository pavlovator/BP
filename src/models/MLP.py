from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from models import prepare as prp
from models import utils
from models import eval

def NN1(x,y):
    '''
    univariate multistep MLP
    :param x: n_steps in of series
    :param y: n_step_out forecast
    :return: model
    '''
    model = Sequential()
    model.add(Dense(60, activation ='tanh', input_dim=24))
    model.add(Dense(72,activation='softplus'))
    model.compile(optimizer= 'Adam', loss='mse')
    model.fit(x, y, epochs=20, verbose=2)
    return model

def NN2(x,y):
    '''
    :param x: multivariate n_steps_in
    :param y: n_step_out forecast
    :return: model
    '''
    model = Sequential()
    model.add(Dense(100, activation='sigmoid', input_dim=6))
    model.add(Dense(72, activation='linear'))
    model.compile(optimizer='Adam', loss='mse')
    model.fit(x, y, epochs=1000, verbose=2)
    return model

def NN3(x,y):
    model = Sequential()
    model.add(Dense(15, activation='sigmoid', input_dim=8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='Adam', loss='mse')
    model.fit(x, y, epochs=50, verbose=2)
    return model

if __name__ == '__main__':
    #====NN1======
    mms = MinMaxScaler()
    mms.fit(prp.DATASET['no2'].values.reshape(-1, 1))
    x,y = prp.prepareNN1(prp.DATASETPO2013,'no2',mms)
    model = NN1(x,y)
    x1, y1 = prp.prepareNN1(prp.DATASETOD2013,'no2', mms)
    preds, reals = eval.evalNN1(x1, y1, model, mms)
    # ====NN2======
    #x,y = prp.prepareNN2(prp.DATASETPO2010, 'no2',1)
    #model = NN2(x,y)
    #=====NN3=====
    #x, y = prp.prepareNN3(prp.DATASETPO2013, 'no2')
    #model = NN3(x,y)
    #x1, y1 = prp.prepareNN3(prp.DATASETOD2013, 'no2')
    #predictionReal = eval.evalNN3Batch(x1,y1,model)
    #====NN3=normalized=====
    #uplne sklamanie cele NN3
    #mms = MinMaxScaler()
    #mms.fit(prp.DATASET['no2'].values.reshape(-1, 1))
    #x, y = prp.prepareNN3(prp.DATASETPO2013, 'no2', mms)
    #model = NN3(x, y)
    #x1, y1 = prp.prepareNN3(prp.DATASETOD2013, 'no2',mms)
    #predictionReal = eval.evalNN3Batch(x1, y1, model)