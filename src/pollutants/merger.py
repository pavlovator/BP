import pandas as pd
NO2 = pd.read_csv("../data/pollutants/NO2_2003_2017.csv",sep=";")
PM10 = pd.read_csv("../data/pollutants/PM10_2003_2017.csv", sep=";")
O3 = pd.read_csv("../data/pollutants/O3_repaired_2003_2017.csv",sep=";")
KOLIBA = pd.read_csv("../data/meteo/st11813.csv", sep='\t')
#LETISKOBA = pd.read_csv("../data/meteo/st11816.csv", sep='\t')
KOSICE = pd.read_csv("../data/meteo/st11968.csv", sep='\t')


MERGE = {"no2m":(NO2,"Bratislava, Trnavské Mýto", KOLIBA),
         "pm10m":(PM10,"Bratislava, Trnavské Mýto", KOLIBA),
         "o3m":(O3,"Košice, Ďumbierska", KOSICE),
        "no2b":(NO2,"Bratislava, Mamateyova", KOLIBA),
         "pm10b":(PM10,"Bratislava, Kamenné nám.",KOLIBA),
         "o3b":(O3,"Bratislava, Jeséniova",KOLIBA)}


def trnavske():
    KOLIBA.rename(columns={"date": "dtvalue"}, inplace=True)
    no2 = NO2[['dtvalue', "Bratislava, Trnavské Mýto"]]
    pm10 = PM10[['dtvalue', "Bratislava, Trnavské Mýto"]]
    df_final = no2.merge(KOLIBA, how='left', on='dtvalue')
    df_final.columns = df_final.columns.str.replace('Bratislava, Trnavské Mýto', 'no2')
    df_final = pd.merge(df_final, pm10, how='outer', on='dtvalue')
    df_final.columns = df_final.columns.str.replace('Bratislava, Trnavské Mýto', 'pm10')
    df_final.columns = map(str.lower, df_final.columns)
    df_final['dd'] = df_final['dd'] / 10
    df_final.to_csv("trnavskemyto" + ".csv", index=False)
    return df_final

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


#merge(MERGE)
