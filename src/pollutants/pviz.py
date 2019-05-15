import matplotlib.pyplot as plt
import random

import matplotlib

matplotlib.use('Qt5Agg')
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
    plt.ylabel(r'$\mu g/m^{3}$')
    if year is not None:
        step = "{:} {:}".format(step, year)
    plt.xlabel(step)
    plt.legend()
    if save != "":
        fig1 = plt.gcf()
        fig1.savefig(save+".png", bbox_inches="tight")
    plt.show()


def visualizeCoverage(pollutants):
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.subplots_adjust(hspace=-1, wspace=0)
    plt.setp(axes,xticks=[])
    for i, j, polidx in ((0, 0, 0), (0, 1, 1), (1, 0, 2), (1, 1, 3)):
        pol = pollutants[polidx]
        minimum = pol.df.loc[0,'dtvalue'].year
        maximum = pol.df.loc[len(pol.df)-1,'dtvalue'].year
        cov = pol.getCoverageOverall().values
        plt.sca(axes[i, j])
        plt.yticks([0,len(cov)-1], [minimum,maximum], fontsize=7)
        plt.xticks([])
        heatmap = axes[i,j].imshow(cov)
        axes[i,j].set_title(pol.getMathTextName())
        axes[i,j].set_xlabel("Stations")
    fig.tight_layout()
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.3, 0.02, 0.4])
    fig.colorbar(heatmap, cax=cbar_ax)

    plt.savefig('coverage.png', dpi=1200)
    plt.show()


no2 = ps.Pollutant("../data/pollutants/NO2_2003_2017.csv", "NO2")
#o3 = ps.Pollutant("../data/pollutants/O3_2003_2017.csv", "O3")
pm10 = ps.Pollutant("../data/pollutants/PM10_2003_2017.csv", "PM10")
#pm25 = ps.Pollutant("../data/pollutants/pm25_2003_2017.csv","PM2.5")
