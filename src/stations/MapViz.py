from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import stations as stat

class MapCreator:
    def __init__(self):
        self.stations = stat.Stations("../data/stanice_shp/stanice_projekt.shp", "../data/stanice_meteo/met_stanice.csv")
        self.map = None
        self.pocetM = 0
        self.pocetP = 0

    def addMeteoStations(self):
        lons = []
        lats = []
        for stanica in self.stations.getStationsMeteo():
            lons.append(stanica.getLongtitude())
            lats.append(stanica.getLatitude())
            self.pocetM+=1
        x, y = self.map(lons, lats)
        self.map.plot(x, y, 'rx', markersize=5)


    def addPollutantStations(self):
        lons = []
        lats = []
        for stanica in self.stations.getStationsPol():
            lons.append(stanica.getLongtitude())
            lats.append(stanica.getLatitude())
            self.pocetP+=1
        x, y = self.map(lons, lats)
        self.map.plot(x, y, 'g+', markersize=6)

    def _buildMap(self,res='l'):
        self.map = Basemap(projection='mill', llcrnrlat=47.65, llcrnrlon=16.77, urcrnrlat=49.65, urcrnrlon=22.65, resolution=res)
        self.map.fillcontinents(color='white', lake_color='blue')
        self.map.drawcountries(color="black")
        self.map.drawrivers(color='blue')



    def showAllStations(self):
        self._buildMap('h')
        self.addMeteoStations()
        self.addPollutantStations()
        plt.tight_layout()
        plt.title("SHMU stations")
        plt.savefig('stations.png', dpi=900)
        plt.show()





if __name__ == '__main__':
    mc = MapCreator()
    mc.showAllStations()

