from bdd import get_database
from insert_datas_db import insert_datas_db

# Fonction permettant de retourner le contenu de la MongoDB ou de la remplir si elle est vide.
# Elle sera utilisée pour transmettre les données au front et former le dashboard
def get_air_quality_datas():
    dbname = get_database()
    collection_name = dbname["air_quality"]
    cur = collection_name.find()   
    results = list(cur)
    #Si la bdd est vide on récupère les données et on return la collection
    #Si la bdd est remplie, on récupère la collection
    if len(results) == 0:
        insert_datas_db()
        return collection_name.find()[0]
    else:
        return collection_name.find()[0]
