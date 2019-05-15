import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

def plotDataset(dataset):
    values = dataset.values
    figure, axes = plt.subplots(nrows=len(dataset.columns), ncols=1)
    for i in range(len(dataset.columns)):
        axes[i].plot(values[:, i])
        axes[i].set_title(dataset.columns[i], y=0.5, loc='right')
    plt.show()

def plotviolinffpppp(dataset):
    sns.set(style="whitegrid")
    ax1 = plt.subplot(121)
    sns.violinplot(data=dataset[['ff']], ax=ax1)
    ax1.set_ylabel('m/s')
    ax3 = plt.subplot(122)
    sns.violinplot(data=dataset[['pppp']], ax=ax3)
    ax3.set_ylabel('hPa')


def plotViolinPols(dataset):
    sns.set(style="whitegrid")
    f, axes = plt.subplots(2, 2)
    sns.violinplot(data=dataset[['ff']], ax=axes[0,0])
    axes[0, 0].set_ylabel('m/s')
    sns.violinplot(data=dataset[['pppp']], ax=axes[0,1])
    axes[0, 1].set_ylabel('hPa')
    sns.violinplot(data=dataset[['no2','pm10']], ax=axes[1,0])
    axes[1, 0].set_ylabel(r'$\mu g/m^{3}$')
    sns.violinplot(data=dataset[['ttt','td']], ax=axes[1,1])
    axes[1, 1].set_ylabel(r'$^\circ$C')

    plt.show()

def plotBar(dataset):
    fq = pd.value_counts(dataset.dd).to_dict()
    new = dict()
    for i in fq:
        new[str(int(i))] = fq[i]
    names = list(new.keys())
    values = list(new.values())
    plt.bar(names, values)
    plt.xlabel('dd')
    plt.show()

def plotAutocorrelation(dataset, numLags):
    cols = ['no2','pm10']
    pols = [r'NO$_{2}$',r'PM$_{10}$']
    font = {'size': 12}
    matplotlib.rc('font', **font)
    f, axes = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.25)
    for i in range(2):
        plt.xlabel('lag')
        plt.ylabel('r')
        plot_acf(dataset[cols[i]], lags=numLags, ax = axes[i], title=pols[i])
    plt.show()

def plotPartialCorrelation(dataset, col , numlags):
    series = dataset[col]
    plot_pacf(series, lags=numlags)
    plt.show()

def pearsonCorrelationMatrix(dataset):
    plt.matshow(dataset[list(set(dataset.columns) - {'dd'})].corr())
    plt.show()


#outlier pm10: 38535:500, 33373:350
dataset = pd.read_csv("cleaned_trnavskeknn.csv", sep=',')
#dataset['dtvalue'] = pd.to_datetime(dataset['dtvalue'])
#dataset.set_index('dtvalue', inplace=True)
#cols = dataset.columns.tolist()
#cols = [cols[-1]] + cols[:-1]
#dataset = dataset[cols]
