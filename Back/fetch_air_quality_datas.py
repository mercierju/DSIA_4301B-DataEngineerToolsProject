import requests
import pandas as pd
from pymongo import MongoClient

# Fonction calculant le nombre total d'observations dans l'API à partir d'une certaine date.
def total_observation(date_debut) :
    response = requests.get("https://services8.arcgis.com/gtmasQsdfwbDAQSQ/arcgis/rest/services/mes_idf_horaire_no2/FeatureServer/0/query", {
        "where": f"nom_dept = 'PARIS' AND date_debut > '{date_debut}'",
        "returnCountOnly": True,
        "f": "json"
    }) 
    data = response.json()
    total = data["count"]
    print(f"There is {total} records")
    return total


# Fonction permettant de récupérer les données de l'API à partir d'une certaine date
def fetch_air_quality_datas(date_debut) : 
    
    total = total_observation(date_debut)

    # response = requests.get("https://services8.arcgis.com/gtmasQsdfwbDAQSQ/arcgis/rest/services/mes_idf_horaire_no2/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json&orderByFields=date_debut%20DESC")
    # wb = response.json()
    # result_requete = pd.json_normalize(wb["features"])
    # last_date_api = result_requete.iloc[0]['attributes.date_debut']/1000 
    
    #Création d'un dataframe avec le nom des colonnes
    response = requests.get("https://services8.arcgis.com/gtmasQsdfwbDAQSQ/arcgis/rest/services/mes_idf_horaire_no2/FeatureServer/0/query?where=nom_dept%20%3D%20%27PARIS%27%20AND%20date_debut%20%3E%3D%20%27"+str(date_debut)+"%27&outFields=*&outSR=4326&f=json")
    wb = response.json()
    intermediaire = pd.json_normalize(wb["features"])
    col = intermediaire.columns
    df  = pd.DataFrame(columns=col)
    i = 0

    #Le serveur de l'API ne permet de récuperer que 2000 observations à la fois
    #On itère donc sur les indexs afin de récupérer les données necessaires et pas que les 2000 premières
    for offset in range(i, total, 2000):
        print(f"Getting element from {offset} to {offset + 2000}")
        #ajouter le date_debut dans la requete
        req = requests.get("https://services8.arcgis.com/gtmasQsdfwbDAQSQ/arcgis/rest/services/mes_idf_horaire_no2/FeatureServer/0/query?where=nom_dept%20%3D%20%27PARIS%27%20AND%20date_debut%20%3E%3D%20%27"+str(date_debut)+"%27&outFields=*&outSR=4326&f=json&ResultOffset="+str(offset))
        # print(req.url)
        wb = req.json()
        df2 = pd.json_normalize(wb["features"])
        frames = [df, df2]
        df = pd.concat(frames,ignore_index=True)

    #Exporter le dataframe au format csv
    df.to_csv('df.csv', sep =';')
    return df
