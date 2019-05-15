import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import json

def load_json(file):
    with open(file, 'r') as fp:
        data = json.load(fp)
    return data

def load_vysledky(which='72'):
    vysledky = {'sn': '', 'MLP':'', 'RNN':'','LSTM':''}
    for model in vysledky.keys():
        no2 = 'jsony_vysledkov/'+model+which+'eNO2.json'
        pm10 = 'jsony_vysledkov/'+model+which+'ePM10.json'
        vysledky[model] = {'no2':load_json(no2), 'pm10':load_json(pm10)}
    vysledky['Seasonal naive'] = vysledky.pop('sn')
    return vysledky

def make_table(vysl,metric):
    matplotlib.rc('xtick', labelsize=12)
    matplotlib.rc('ytick', labelsize=12)
    time = list(range(72))
    polsidx = ['no2','pm10']
    pols = [r'NO$_{2}$',r'PM$_{10}$']
    plt.figure(figsize=(12,6))
    plt.subplots_adjust(hspace=0.5, top=0.935, bottom=0.1,left=0.065, right=0.99)
    for i in range(2):
        plt.subplot(2,1,1+i)
        for model in vysl.keys():
            plt.plot(time, vysl[model][polsidx[i]][metric])
            plt.title(pols[i], fontdict={'fontsize':20})
            plt.legend(tuple(vysl.keys()), loc='upper right')
            plt.xticks(list(range(0,72,8)))
        plt.axvline(x=23, color='black', linewidth=0.6)
        plt.axvline(x=47, color='black', linewidth=0.6)
        plt.xlabel('hours', fontsize=16)
        if metric == 'r':
            plt.ylabel('r', fontsize=16)
        else:
            plt.ylabel(metric.upper(), fontsize=16)
    plt.savefig('vysl72/{:}.png'.format(metric), dpi=300)
    plt.show()



vysledky = load_vysledky()
