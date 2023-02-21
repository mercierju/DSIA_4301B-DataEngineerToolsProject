from pymongo import MongoClient

#Initialisation de la bdd
def get_database():
   client = MongoClient(host='mongodb',
                        port=27017, 
                        username='root', 
                        password='password',
                        authSource="admin")
   # client = MongoClient(host='localhost', port=27017)
   return client['data_engineering']


