import pandas as pd
import json
import datetime
from bdd import get_database
from fetch_air_quality_datas import fetch_air_quality_datas

# Fonction permettant de convertir les données au format csv en format json qui sera plus adapté pour structurer notre
# MongoDB.
def convert_air_quality_datas_to_json() :
    #Récupération des données
    fetch_air_quality_datas('2021-01-01')

    df = pd.read_csv("df.csv",delimiter=';')
    df = df.replace('Bld Périphérique Est','Bld Peripherique Est')
    df = df.replace("Place de l'Opéra","Place de l Opera")
    #Convertion des timestamps unix en date lisible
    df["attributes.date_debut"] = df["attributes.date_debut"]/1000
    df["date"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)))
    df["year"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).year)
    df["month"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).month)
    df["day"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).day)


    def pd_to_station_dict(df):
        for (station), df_station_grouped in df.groupby(["attributes.nom_station"]):
            print(station)
            yield {station: {
                "Arr": df.loc[df['attributes.nom_station'] == station, 'attributes.nom_com'].iloc[0],
                "Id_com" : int(df.loc[df['attributes.nom_station'] == station, 'attributes.id_com'].iloc[0]),
                "Longitude" : df.loc[df['attributes.nom_station'] == station, 'geometry.x'].iloc[0],
                "Latitude" : df.loc[df['attributes.nom_station'] == station, 'geometry.y'].iloc[0],
                "Mesures" : list(split_mesures(df_station_grouped))
                }
            }

    def split_mesures(df_station_grouped):
        for row in df_station_grouped.itertuples():
            yield {
                "Annee" : row[22],
                "Mois" : row[23],
                "Jour" : row[24],
                "Heure" : row[21].hour,
                "Date" : str(row[21]),
                "Date_exacte" : row[14],
                "Nom_Poll": row[9],
                "Id_Poll": int(row[10]),
                "Valeur": int(row[11]),
                "Unite": row[12],
                "Typologie": row[8]
            }

    station_list = list(pd_to_station_dict(df))
    station_dict = {}
    for sub_dict in station_list:
        station_dict.update(sub_dict)

    fichier = open("df_json.json", "w")
    json.dump(station_dict,fichier ,indent=4)
    fichier.close()

# Fonction permettant d'inserer les données au format json dans la MongoDB
def insert_datas_db() :
    dbname = get_database()
    convert_air_quality_datas_to_json()
    with open('df_json.json') as f:
        json_datas = json.load(f)
    collection_name = dbname["air_quality"]
    collection_name.insert_one(json_datas)

# convert_air_quality_datas_to_json()

