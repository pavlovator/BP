import pandas as pd
import matplotlib.pyplot as plt
import random

class Pollutant:
    def __init__(self, path, name):
        self.df = pd.read_csv(path, sep=';')
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        self.name = name

    def getName(self):
        '''
        :return: nazov znecistujucej latky
        '''
        return self.name

    def getStations(self):
        '''
        :return: nazvy vsetkych stanic
        '''
        return self.df.keys()

    def getStationDF(self, station):
        '''
        :param station: nazov stanice
        :return: dataframe namerancyh hodinovych koncentracii pre stanicu
        '''
        if station not in self.df.keys():
            raise Exception('station: {:} does not exist in {:} data'.format(station, self.name))
        return self.df.loc[:, ['dtvalue', station]]


    def hourProfile(self, station, year=None):
        '''
        :param station: nazov stanice
        :param year: pre ktory rok, ak nieje uvedeny tak pre vsetky
        :return: dataframe denneho profilu
        '''
        df_station = self.getStationDF(station).dropna()
        if year is not None:
            df_station = df_station[df_station['dtvalue'].dt.year == year]
        return df_station.groupby(df_station["dtvalue"].dt.hour).mean()

    def monthProfile(self,station, year=None):
        '''
        :param station: nazov stanice
        :param year: pre ktory rok, ak nieje uvedeny tak pre vsetky
        :return: dataframe rocneho profilu
        '''
        df_station = self.getStationDF(station).dropna()
        if year is not None:
            df_station = df_station[df_station['dtvalue'].dt.year == year]
        return df_station.groupby(df_station["dtvalue"].dt.month).mean()

    def dayProfile(self, station, year=None):
        df_station = self.getStationDF(station).dropna()
        if year is not None:
            df_station = df_station[df_station['dtvalue'].dt.year == year]
        return df_station.groupby(df_station["dtvalue"].dt.weekday).mean()

    def commonStation(self, particles):
        '''
        :param particles: list Particles
        :return: mnozina vsetkych spolocnych stanic pre danu latku a latky v liste particles
        '''
        stations = set(self.getStations())
        for p in particles:
            stations &= set(p.getStations())
        return stations

    def getCoverageOverall(self):
        '''
        :return: vytaznost dat po rokoch pre vsetky stanice
        '''
        by_year = self.df.groupby(self.df['dtvalue'].dt.year).apply(lambda x: x.notnull().mean()*100)
        del by_year['dtvalue']
        return by_year.mean(axis=1)

    def getCoverageByStation(self,station):
        '''
        :param station: nazov stanice
        :return: vytaznoc po rokoch pre konkretnu stanicu
        '''
        df_station = self.getStationDF(station)
        avarage = df_station.groupby(df_station['dtvalue'].dt.year).apply(lambda x: x.notnull().mean()*100)
        del avarage['dtvalue']
        return avarage

    def get_training_data(self, station):
        df_station = self.getStationDF(station)

















def visualizeTimeProfile(step, pollutants, station, year=None, save=""):
    '''
    :param step: jednotka casu
    :param pollutants: list Pollutants
    :param station: nazov stanice
    :param save: nazov suboru na ulozenie ak nie je dany tak sa neulozi
    :return:
    '''
    if type(pollutants) != list:
        raise Exception("argument 'particles' is not a list")
    if step not in 'hours months days'.split():
        raise Exception('time step: {:} definied'.format(step))
    for p in pollutants:
        line_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if step == 'hours':
            y = p.hourProfile(station)
        elif step == 'months':
            y = p.monthProfile(station)
        elif step == 'days':
            y = p.dayProfile(station)
        plt.plot(y.index.values, y[station].values, color=line_color, label = p.getName())
    plt.xticks(y.index.values)
    plt.title(station)
    plt.grid(True)
    plt.ylabel("concentrations")
    if year is not None:
        step = "{:} {:}".format(step, year)
    plt.xlabel(step)
    plt.legend()
    if save != "":
        fig1 = plt.gcf()
        fig1.savefig(save+".png", bbox_inches="tight")
    plt.show()


