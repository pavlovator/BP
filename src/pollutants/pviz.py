import matplotlib.pyplot as plt
import random
import pollutants as ps

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


def visualizeCoverage(pollutants):
    fig = plt.figure()
    fig.subplots_adjust(hspace=-0.6, wspace=0.15)
    for i,pol in enumerate(pollutants):
        ax = fig.add_subplot(2, 2, i+1)
        ax.set_xticks([])
        ax.set_yticks([])
        heatmap = ax.imshow(pol.getCoverageOverall().values)
        ax.set_title(pol.getName())
        ax.set_xlabel("Stations")
        ax.set_ylabel("Years")

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.02, 0.5])
    fig.colorbar(heatmap, cax=cbar_ax)

    plt.savefig('coverage.png', dpi=900)
    plt.show()
    return cbar, fig


no2 = ps.Pollutant("../data/pollutants/NO2_2003_2017.csv", "NO2")
o3 = ps.Pollutant("../data/pollutants/O3_2003_2017.csv", "O3")
pm10 = ps.Pollutant("../data/pollutants/PM10_2003_2017.csv", "PM10")
pm25 = ps.Pollutant("../data/pollutants/pm25_2003_2017.csv","PM2.5")

cbar,fig = visualizeCoverage([no2,o3,pm10,pm25])