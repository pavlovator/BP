import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

def resample(path, to='D'):
    df = pd.read_csv(path, sep=',')
    df['dtvalue'] = pd.to_datetime(df['dtvalue'])
    df = df.set_index('dtvalue')
    pols = df[['no2','pm10']]
    pols = pols.resample(to).mean()
    pols['dtvalue'] = pols.index
    return pols



path = "trnavskemytoImp.csv"