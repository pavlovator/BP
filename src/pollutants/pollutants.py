import pandas as pd

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

    def getMathTextName(self):
        '''
        :return: Math text name for pollutant
        '''
        idx = 0
        for i in range(len(self.name)):
            if self.name[i].isnumeric():
                idx = i
                break
        return r'$'+self.name[:idx]+'_{'+self.name[idx:] +'}$'

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
        '''
        :param station: nazov stanice
        :param year: pre ktory rok, ak nieje uvedeny tak pre vsetky
        :return: dataframe tyzdenneho profilu
        '''
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
        return by_year

    def getCoverageByStation(self,station):
        '''
        :param station: nazov stanice
        :return: vytaznoc po rokoch pre konkretnu stanicu
        '''
        df_station = self.getStationDF(station)
        avarage = df_station.groupby(df_station['dtvalue'].dt.year).apply(lambda x: x.notnull().mean()*100)
        del avarage['dtvalue']
        return avarage

    def selectBestByCoverage(self,treshold = 0):
        result = dict()
        for station in self.df.keys()[1:]:
            points = 0
            station_coverage = self.getCoverageByStation(station)
            for percentage in station_coverage.values:
                points += percentage[0]
            points = points/15
            if points > treshold:
                result[station] = points #15 rokov
        return result

