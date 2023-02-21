from pymongo import MongoClient
import datetime
from fetch_air_quality_datas import fetch_air_quality_datas
import pandas as pd
from bdd import get_database
from fetch_air_quality_datas import total_observation

# Fonction qui  permet de mettre a jour les données si il y en a plus sur l'API que dans la MongoDB
# en récupérant les données de l'API a partir de la date de la dernière observation dans la BDD
# Si les données récupérées sont vides, il n'y a pas d'update, si il en a, on les récupère et on les push dans la bdd
# en fonction de la station de prélèvement
# Return 'UPDATE' si update, 'NO UPDATE' sinon
def update_datas_db() :
    dbname = get_database()
    collection_name = dbname["air_quality"]

    date_lenglen = datetime.datetime.fromtimestamp(collection_name.find()[0]["PARIS stade Lenglen"]["Mesures"][-1]["Date_exacte"]).isoformat()
    date_bonaparte= datetime.datetime.fromtimestamp(collection_name.find()[0]["Rue Bonaparte"]["Mesures"][-1]["Date_exacte"]).isoformat()
    date_opera= datetime.datetime.fromtimestamp(collection_name.find()[0]["Place de l Opera"]["Mesures"][-1]["Date_exacte"]).isoformat()
    date_periph= datetime.datetime.fromtimestamp(collection_name.find()[0]["Bld Peripherique Est"]["Mesures"][-1]["Date_exacte"]).isoformat()
    dates = [date_opera, date_bonaparte, date_lenglen, date_periph]
    last_date = max(dates)
    print(last_date)

    total = total_observation(last_date)

    if total != 0 :

        fetch_air_quality_datas(last_date)

        df = pd.read_csv("df.csv",delimiter=';')

        df = df.replace('Bld Périphérique Est','Bld Peripherique Est')
        df = df.replace("Place de l'Opéra","Place de l Opera")
        #Convertion des timestamps unix en date lisible
        df["attributes.date_debut"] = df["attributes.date_debut"]/1000
        df["date"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)))
        df["year"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).year)
        df["month"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).month)
        df["day"] = df["attributes.date_debut"].apply(lambda x : datetime.datetime.fromtimestamp(int(x)).day)


        for row in df.itertuples():
            station = row[6]
            mesure = {
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
            collection_name.update_one(
            {},
            {"$push":{str(station)+".Mesures": mesure}}
            )
        
        return 'UPDATE'
        
    else : 
        return 'NO UPDATE'

# update_datas_db()