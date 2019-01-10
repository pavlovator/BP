import geopandas as gpd
import pandas as pd

from math import sin, cos, radians, acos


class Stations:
    class StationPol:
        def __init__(self, series):
            '''
            :param series: pandas series of station attributes
            '''
            self.station = series.to_dict()

        def getName(self):
            '''
            :return: name of station
            '''
            return self.station['Umiestneni']

        def getLongtitude(self):
            '''
            :return: longtitude of station
            '''
            return self.station['X']

        def getLatitude(self):
            '''
            :return: latitude of station
            '''
            return self.station['Y']

        def getTypeStation(self):
            '''
            :return: type of station
            '''
            return self.station['Typ stanic']

        def getTypeLocation(self):
            '''
            :return: type of geographic location for station
            '''
            return self.station['Typ oblast']

    class StationMeteo:
        def __init__(self, series):
            self.station = series.to_dict()

        def getIndikativ(self):
            return self.station['Indikativ']

        def getName(self):
            return self.station['Stanica']

        def getLongtitude(self):
            '''
            :return: longitude of station
            '''
            return self.station['Zem.dlzka']

        def getLatitude(self):
            '''
            :return: latitude of station
            '''
            return self.station['Zem.sirka']

        def getZemVyska(self):
            return self.station['Nadm.vyska']



    def __init__(self, pathPol, pathMeteo):
        '''
        :param path: shapefile stations path
        '''
        self.stationsPol = gpd.read_file(pathPol, encoding='UTF-8')
        self.stationsMeteo = pd.read_csv(pathMeteo,sep=';')

    def getStationsPol(self):
        '''
        :return: list of pollutant Stations
        '''
        stations_list = []
        for i in range(len(self.stationsPol)):
            stations_list.append(self.StationPol(self.stationsPol.iloc[i]))
        return stations_list

    def getStationsMeteo(self):
        ''''
        list of meteo station
        '''
        stations_list = []
        for i in range(len(self.stationsMeteo)):
            stations_list.append(self.StationMeteo(self.stationsMeteo.iloc[i]))
        return stations_list

    def _distance(self,point1, point2):
        '''
        :param point1: (lon,lat)
        :param point2: (lon,lat)
        :return: Haversine formula distance between 2 points on map
        '''
        R = 6371.01
        slat = radians(point1[1])
        slon = radians(point1[0])
        elat = radians(point2[1])
        elon = radians(point2[0])

        distance = R * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
        return distance

    def getPollutantToMeteoDistances(self,treshold = float('inf'), elevation550 = 550):
        '''

        :param treshold: distance smaller than
        :return: distances between pollutant stations and meteo stations 1:N
        '''
        polStat = self.getStationsPol()
        meteoStat = self.getStationsMeteo()
        result = dict()
        pozadove = dict()
        dopravne = dict()
        result["pozadove"] = pozadove
        result["dopravne"] = dopravne
        for ps in polStat:
            k = dict()
            for ms in meteoStat:
                dist = self._distance((ps.getLongtitude(),ps.getLatitude()),(ms.getLongtitude(),ms.getLatitude()))
                if dist <= treshold and ms.getZemVyska() <= elevation550:
                    k[ms.getName()] = dist
            if len(k) != 0:
                if ps.getTypeStation() == 'B':  # pozadova
                    pozadove[ps.getName()] = k
                elif ps.getTypeStation() == 'T':  # dopravna
                    dopravne[ps.getName()] = k
        return result

STATIONS = Stations("../data/stanice_shp/stanice_projekt.shp","../data/stanice_meteo/met_stanice.csv")