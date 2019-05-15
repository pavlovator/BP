import pandas as pd
import numpy as np

class Calc:
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def count(self, feature):
        return len(self.df[feature])

    def missPercentage(self, feature):
        return self.df[feature].isnull().sum() / self.df[feature].shape[0] * 100.00

    def cardinality(self, feature):
        return self.df[feature].nunique()

    def minimum(self, feature):
        return self.df[feature].min()

    def maximum(self, feature):
        return self.df[feature].max()

    def mean(self, feature):
        return self.df[feature].mean()

    def median(self, feature):
        return self.df[feature].median()

    def stdDev(self, feature):
        return self.df[feature].std()

    def quartile1(self, feature):
        return np.nanpercentile(self.df[feature], 25)

    def quartile3(self, feature):
        return np.nanpercentile(self.df[feature], 75)

    def mode(self, feature):
        return self.df[feature].mode().values[0]

    def modeFreq(self, feature):
        return self.df[feature].value_counts()[self.df[feature].mode().values[0]]

    def modePerc(self, feature):
        return self.df[feature].value_counts(normalize=True)[self.df[feature].mode().values[0]]

    def mode2(self, feature):
        return self.df[feature].value_counts().index.tolist()[1]

    def mode2Freq(self, feature):
        return self.df[feature].value_counts()[1]

    def mode2Perc(self, feature):
        return self.df[feature].value_counts(normalize=True).tolist()[1]

    def forContinuous(self, feature):
        return [self.count(feature),
                round(self.missPercentage(feature),2),
                self.cardinality(feature),
                round(self.minimum(feature),4),
                round(self.quartile1(feature),2),
                round(self.mean(feature),2),
                round(self.median(feature),2),
                round(self.quartile3(feature),2),
                round(self.maximum(feature),2),
                round(self.stdDev(feature),2)]

    def forCategorical(self, feature):
        return [self.count(feature),
                round(self.missPercentage(feature),2),
                self.cardinality(feature),
                self.mode(feature),
                self.modeFreq(feature),
                round(self.modePerc(feature)*100,2),
                self.mode2(feature),
                self.mode2Freq(feature),
                round(self.mode2Perc(feature)*100,2)]

    def coverageOfFeatures(self):
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        by_year = self.df.groupby(self.df['dtvalue'].dt.year).apply(lambda x: x.notnull().mean() * 100)
        del by_year['dtvalue']
        return by_year

    def nomofmissingPreYear(self):
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        by_year = self.df.groupby(self.df['dtvalue'].dt.year).apply(lambda x: x.notnull().size())
        del by_year['dtvalue']
        return by_year

    def percentageOfMissingLoners(self):
        for label in self.df.columns:
            counter = 0
            last = np.nan
            next = np.nan
            col = self.df[label]
            if label == 'dtvalue':
                continue
            for i in range(len(col)-1):
                current = col[i]
                next = col[i+1]
                if np.isnan(current) and not np.isnan(last) and not np.isnan(next):
                    counter += 1
                last = current
            print(label, counter/len(self.df)*100, counter)


def createLatexABTTable(path):
    dataset = Calc(path)
    s = ""
    for feature in ['pm10','no2','ttt','td','ff','pppp']:
        s += "{:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:}".format(feature,*dataset.forContinuous(feature))
    s += "{:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:}".format("dd",*dataset.forCategorical("dd"))
    return s







trnavske = Calc("trnavskemyto.csv")