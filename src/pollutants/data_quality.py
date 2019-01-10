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
        return np.nanpercentile(self.df[feature], 25)

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


def createLatexABTTable(path):
    dataset = Calc(path)
    s = ""
    for feature in ['pol','ttt','td','ff','pppp']:
        s += "{:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:}".format(feature,*dataset.forContinuous(feature))
    s += "{:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:} & {:}".format("dd",*dataset.forCategorical("dd"))
    return s





no2m = "no2m.csv"
pm10m = "pm10m.csv"
o3m = "o3m.csv"