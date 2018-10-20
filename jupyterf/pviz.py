import pandas as pd
import matplotlib.pyplot as plt
import random



class Particle:
    def __init__(self, path, name):
        self.df = pd.read_csv(path, sep=';')
        self.df['dtvalue'] = pd.to_datetime(self.df['dtvalue'])
        self.name = name

    def getName(self):
        return self.name

    def getStations(self):
        return self.df.keys()

    def getStationDF(self, station):
        if station not in self.df.keys():
            raise Exception('station: {:} does not exist in {:} data'.format(station, self.name))
        return self.df.loc[:, ['dtvalue', station]]


    def hourProfile(self, station):
        df_station = self.getStationDF(station).dropna()
        return df_station.groupby(df_station["dtvalue"].dt.hour).mean()

    def monthProfile(self,station):
        df_station = self.getStationDF(station).dropna()
        return df_station.groupby(df_station["dtvalue"].dt.month).mean()


    def commonStation(self, particles):
        '''
        :param particles: list Particles
        :return: mnozina vsetkych spolocnych stanic pre danu latku a latky v liste particles
        '''
        stations = set(self.getStations())
        for p in particles:
            stations &= set(p.getStations())
        return stations

    def getCollectedYearOverall(self):
        by_year = self.df.groupby(self.df['dtvalue'].dt.year).apply(lambda x: x.notnull().mean()*100)
        del by_year['dtvalue']
        return by_year.mean(axis=1)

    def getCollectedByStation(self,station):
        df_station = self.getStationDF(station)
        avarage = df_station.groupby(df_station['dtvalue'].dt.year).apply(lambda x: x.notnull().mean()*100)
        del avarage['dtvalue']
        return avarage

















def visualizeTimeProfile(step, particles, station, save=""):
    '''
    :param step: jednotka casu
    :param particles: list Particles
    :param station: nazov stanice
    :param save: nazov suboru na ulozenie ak nie je dany tak sa neulozi
    :return:
    '''
    if type(particles) != list:
        raise Exception("argument 'particles' is not a list")
    if step not in 'hours months'.split():
        raise Exception('time step: {:} definied'.format(step))
    for p in particles:
        line_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if step == 'hours':
            y = p.hourProfile(station)
        elif step == 'months':
            y = p.monthProfile(station)
        plt.plot(y.index.values, y[station].values, color=line_color, label = p.getName())
    plt.xticks(y.index.values)
    plt.title(station)
    plt.grid(True)
    plt.ylabel("concentrations")
    plt.xlabel(step)
    plt.legend()
    if save != "":
        fig1 = plt.gcf()
        fig1.savefig(save+".png", bbox_inches="tight")
    plt.show()


