import requests
import pandas as pd

def get_tree_datas() :
    # - Récupération des données d'arbres
    # On effectue une requette vers l'API de notre dataset
    req = requests.get("https://opendata.paris.fr/api/records/1.0/search/?dataset=les-arbres-plantes&q=&rows=3008")
    wb = req.json()

    # -- Création et normalisation du dataframe :
    # On stocke les données récupérées dans une dataframe panda
    df = pd.json_normalize(wb["records"])
    # On supprime les collones inutiles
    df.drop("datasetid",inplace = True, axis=1)
    df.drop("recordid",inplace = True, axis=1)
    df.drop("fields.genre",inplace = True, axis=1)
    df.drop("fields.varieteoucultivar",inplace = True, axis=1)
    df.drop("fields.complementadresse",inplace = True, axis=1)
    df.drop("fields.domanialite",inplace = True, axis=1)
    df.drop("fields.espece",inplace = True, axis=1)
    # On supprime les lignes comportant des valeurs manquantes
    df = df.dropna()
    # On renomme les arrondissements afin de les avoir sous la même forme que ceux compris dans notre base de donnée
    def rename_arrondissement(arr):
        return arr.replace('PARIS ', 'PARIS-').replace(' ARRDT', '-ARRONDISSEMENT')
    df['fields.arrondissement'] = df['fields.arrondissement'].apply(rename_arrondissement)

    return df