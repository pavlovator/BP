import pandas as pd
NO2 = pd.read_csv("../data/pollutants/NO2_2003_2017.csv",sep=";")
PM10 = pd.read_csv("../data/pollutants/PM10_2003_2017.csv", sep=";")
O3 = pd.read_csv("../data/pollutants/O3_repaired_2003_2017.csv",sep=";")
KOLIBA = pd.read_csv("../data/meteo/st11813.csv", sep='\t')
KOSICE = pd.read_csv("../data/meteo/st11968.csv", sep='\t')


MERGE = {"no2m":(NO2,"Bratislava, Trnavské Mýto", KOLIBA),
         "pm10m":(PM10,"Bratislava, Trnavské Mýto", KOLIBA),
         "o3m":(O3,"Košice, Ďumbierska", KOSICE),
        "no2b":(NO2,"Bratislava, Mamateyova", KOLIBA),
         "pm10b":(PM10,"Bratislava, Kamenné nám.",KOLIBA),
         "o3b":(O3,"Bratislava, Jeséniova",KOLIBA)}



def merge(files):
    for name in files:
        pol, station, meteo, = files[name]
        onlyStation = pol[['dtvalue', station]]
        new = onlyStation.merge(meteo, left_on='dtvalue', right_on='date', how='left')
        new = new.drop(columns=['date'])
        new.rename(columns={station:"pol"}, inplace=True)
        new.columns = map(str.lower, new.columns)
        new['dd'] = new['dd']/10
        new.to_csv(name+".csv",index=False)


merge(MERGE)

