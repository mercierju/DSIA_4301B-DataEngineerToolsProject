# La qualité de l'air et les arbres dans Paris

## Description du projet

Beaucoup de villes sont de plus en plus bétonnées et laissent moins de place à la végétation et aux arbres, et Paris ne fait pas exception à la règle. De plus, la qualité de l'air dans la capitale est en permanente dégradation, et des épisodes de pollution sont plus fréquents au fil du temps.
C'est pourquoi il est important de planter des arbres pour rendre les villes plus vertes.
Le feuillage des arbres est recouvert de pores qui captent les particules fines dont le dioxyde de carbone et le dioxyde d’azote (NO2) contenus dans l’air. Ils les emprisonnent et rejettent de l’oxygène: c’est le processus de photosynthèse. 


Quelques statistiques liées aux mesures des N02 et au nombre d'arbres plantés pourront peut-être vous éclairer sur le sujet.


Problématique: Comment à évolué la quantité de NO2 dans l'air de Paris au cours des dernières années ? Y a-t-il un lien avec la quantité de nouveaux arbres plantés ?


## User Guide

### Installation de Git et récupération des fichiers

Pour avoir un bon fonctionnement du projet, il faut vérifier que vous avez bien installé [Git](https://git-scm.com/) sur votre espace de travail afin de récupérer les fichiers.
Ensuite, il faut cloner le repository dans le dossier local souhaité en utilisant la commande `git clone https://github.com/mercierju/DSIA_4301B-DataEngineerToolsProject.git` afin d'avoir accès au répertoire.

Le code s'organise en plusieurs conteneurs, permettant de gérer des fonctionnalités différentes. Il vous faudra donc vérifier que vous avez bien installé Docker.

Une fois notre repository cloné sur votre machine, il faudra exécuter la commande `docker compose up -d` à la racine du projet. Cela va construire les conteneurs nécessaires au fonctionnement de l'application ainsi que les démarrer.

Pour voir le dashboard, il faut aller sur votre navigateur et mettre `http://localhost:8000/`. (ça mettra un peu de temps à charger, environ une minute)

Si les conteneurs ont déjà été créés auparavant, pour les démarrer
### Les données utilisées

Pour pouvoir répondre à la problématique, nous utilisons :
- https://data-airparif-asso.opendata.arcgis.com/datasets/airparif-asso::mes-idf-horaire-no2/explore?location=48.808454%2C2.383873%2C11.62&showTable=true 
Nous récupérons les données grâce à l'API

- https://opendata.paris.fr/explore/dataset/les-arbres-plantes/table/?location=11,48.83375,2.34318&basemap=jawg.streets
Nous récupérons les données grâce à l'API

- https://www.iqair.com/fr/france/ile-de-france/paris 
Nous récupérons les données en scrappant la page

### Les paquets à utiliser

Des paquets sont nécessaires pour le bon fonctionnement du projet, ils sont dans les fichiers requirements.txt, et sont automatiquement installés dans les conteneurs correspondants lors de leur création.


### Fonctionnement du projet

Le projet est divisé en 3 composants principaux : 
- la base de donnée MongoDB qui permet de stocker les données
- le front qui permet d'afficher les données sous forme de dashboard
- le back qui permet la gestion d'une base de données. Pour ça il faut récupérer  les données, les convertir en format json, les push dans la base de donnée, initialiser celle-ci, actualiser les données si nécessaire, faire le lien avec le front pour lui transmettre les données.



Mais concrètement, comment ça marche ?

Lorsque nous exécutons notre application pour la première fois, nous récupérons les données liées à la pollution de l'air via une API. Nous convertissons ces données en JSON afin de les mettre dans la base de données sous une forme plus structurée qu'un simple dataframe. Nous avons décidé de regrouper les mesures par stations qui sont au nombre de 4. Nous faisons ces opérations dans le back.

Une fois les données mises dans la base de données MongoDB, il faut les afficher ces données. Nous le faisons sous forme de Dashboard. Cette partie est faite dans le front.

En complément de ces données, nous récupérons des données liées aux arbres qui sont plantés dans Paris depuis 2020, que nous récupérons par une API, ainsi que des données en temps réel de la qualité de l'air dans Paris, qui sont scrappées. Ces données sont ensuite couplées avec les données de notre base de données. Ces opérations sont faites dans le front, car nous ne stockons pas ces informations dans une base de données.

Sur le dashboard, il y a un bouton 'Update datas in the database', qui permet de mettre à jour les données dans la base de données si on le souhaite. L'API est alimenté chaque jour par de nouvelles données. Ainsi, cliquer sur ce bouton permet de mettre à jour la base de données en ajoutant les données manquantes, et de rafraîchir la page afin d'afficher les graphs avec les données mises à jour.


## Developer Guide 

Le projet est divisé en 3 conteneurs : le front, le back, et la base de données.

La base de données MongoDB nous servira à stocker les données.

Le front sert à former les graphiques et afficher le dashboard :
- former le dashboard : `dashboard.py`
- scrapper des données en temps réel sur la qualité de l'air : `scrap_iqair.py`
- récupérer des données sur la plantation d'arbres dans Paris : `tree_api.py`
- les requirements pour ce container : `requirements.txt`
- le Dockerfile de ce conteneur : `Dockerfile`


Le back sert à :
- gérer la partie récupération des données : `fetch_air_quality_datas.py`
- convertir les données en format json et insérer les données dans la base de donnée : `insert_datas_db.py`
- initialiser la base de donnée : `bdd.py`
- update les données s'il y en a des nouvelles dans l'API : `update_datas_bdd.py`
- récupérer les données stockées dans la base de donnée : `get.py`
- faire le lien entre le back et le front afin que l'utilisateur puisse update les données à partir de l'interface : `app.py`
- les requirements pour ce conteneur : `requirements.txt`
- le Dockerfile de ce container : `Dockerfile`

La configuration permettant d'initialiser et de lancer le projet est stockée dans le fichier : `docker-compose.yml`.


## Rapport d'analyse
On peut voir qu'en moyenne, la station la plus polluée est la station du périphérique Est, ce qui semble assez logique étant donné la circulation importante et les embouteillages sur cet axe de circulation.
La plantation d'arbres semble influer sur la qualité de l'air, cependant, il y a de nombreux paramètres à prendre en compte, et il est difficile de déterminer une corrélation entre la plantation d'arbres et la qualité de l'air à Paris.
Dans tous les cas, il est bénéfique de végétaliser la capitale.



