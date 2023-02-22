# La qualité de l'air et les arbres dans Paris

## Description du projet

Beaucoup de villes sont de plus en plus bétonnées et laissent moins de place à la végétation et aux arbres, et Paris ne fait pas exception à la règle. De plus, la qualité de l'air dans Paris est en permanente dégradation, et des épisodes de pollution sont plus fréquents au fil du temps.
C'est pourquoi il est important de planter des arbres pour rendre les villes plus vertes.
Le feuillage des arbres est recouvert de pores qui captent les particules fines dont le dioxyde de carbone et le dioxyde d’azote (NO2) contenus dans l’air. Ils les emprisonnent et rejettent de l’oxygène: c’est le processus de photosynthèse. 

Notre association (fictive...) se bat pour une campagne de plantation d'arbreq et de végétalisation de Paris plus active !

Quelques statistiques pourront vous convaincre de nous suivre...


Problématique: Comment à évolué la quantité de NO2 dans l'air de Paris au cours des dernières années ? Y a t-il un lien avec la quantité de nouveaux arbres plantés ?


## User Guide

### Installation de Git et récupération des fichiers

Pour avoir un bon fonctionnement du projet, il faut vérifier que vous avez bien installé [Git](https://git-scm.com/) sur votre espace de travail afin de récupérer les fichiers.
Ensuite, il faut cloner le repository dans le dossier local souhaité en utilisant la commande `git clone https://github.com/mercierju/DSIA_4301B-DataEngineerToolsProject.git` afin d'avoir accès au répertoire.

Le code s'organise en plusieurs conteneurs, permettant de gérer des fonctionnalités différentes. Il vous faudra donc verifier que vous avez bien installé Docker.

Une fois notre repository cloné sur votre machine, il faudra executer la commander `docker compose up -d` à la recine du projet.

### Le dataset à utiliser

Pour pouvoir répondre à la problématique, nous utilisons :
- https://data-airparif-asso.opendata.arcgis.com/datasets/airparif-asso::mes-idf-horaire-no2/explore?location=48.808454%2C2.383873%2C11.62&showTable=true 
Nous récupérons les données grâce à l'API

- https://opendata.paris.fr/explore/dataset/les-arbres-plantes/table/?location=11,48.83375,2.34318&basemap=jawg.streets
Nous récupérons les données grâce à l'API

- https://www.iqair.com/fr/france/ile-de-france/paris 
Nous récupérons les données en scrappant la page

### Les paquets à utiliser

Des paquets sont nécessaires pour le bon fonctionnement du projet, ils sont dans les fichers requirements.txt, et sont automatiquement installés dans les conteneurs correspondants lors de leur créations.


### Fonctionnement du projet

Le projet est divisé en 3 composants principaux : 
- la base de donnée MongoDB qui permet de stocker les données
- le front qui permet d'afficher les données sous forme de dashboard
- le back qui permet de récupérer les données, les convertir en format json, les push dans la base de donnée, initialiser celle-ci, update les données si nécessaire, faire le lien avec le front pour lui transmettre les données.

Le dataset en ligne étant mis à jour tous les jours, il y a sur le dashboard un bouton permettant d'update les données de la base de donnée Mongo si elle n'est pas à jour.

Blablabla sur le Dashboard


## Developer Guide 

Le projet est divisé en 3 conteneurs : le front, le back, et la base de donnée.

La base de donnée MongoDB nous servira à stocker les données.

Le front sert à former les graphiques et afficher le dashboard :
- former le dashboard : `dashboard.py`
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
On peut voir qu'en moyenne, la station la plus poluée est la station du périférique Est, ce qui semble assez logique étant donné la circulation importante et les embouteillages sur cet axe de circulation.


