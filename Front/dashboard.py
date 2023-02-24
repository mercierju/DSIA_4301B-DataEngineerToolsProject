import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly_express as px
import requests
import dash
from dash.dependencies import Output, Input
import numpy as np
import folium 
from folium.plugins import MarkerCluster
import datetime
from scrap_iqair import get_tables
from tree_api import get_tree_datas


# -- Récupération des données par le front

# - Récupération des données de pollution
air_quality_datas = requests.get('http://back:5000/get_air_quality_datas')
# air_quality_datas = requests.get('http://localhost:5000/get_air_quality_datas')
data_json = air_quality_datas.json()


# -- Récuppération des données par scrapping

# - Récupération des infos de pollution en temps réel
main_poll_table,other_poll_table = get_tables()


# -- Récupération des données par API

# - Récupération des données d'arbres
df = get_tree_datas()


# fonction appelée par un bouton du front qui trigger le back pour update les données
# return 'UPDATE s'il y a des données a mettre à jour, 'NO UPDATE' sinon
def update_bdd():
    update_datas = requests.get('http://back:5000/update_bdd')
    # update_datas = requests.get('http://localhost:5000/update_bdd')
    return update_datas.text



#BARCHART
mean_station=[]
name_stations = ['Bld Peripherique Est','PARIS stade Lenglen','Place de l Opera', 'Rue Bonaparte']
values = []
for j in name_stations :
    for i in range(0,len(data_json[j]['Mesures'])) : 
        values.append(data_json[j]['Mesures'][i]['Valeur'])
    mean_station.append(np.mean(values))

data = {'station': name_stations,'valeur_moyenne en ug.m-3': mean_station}
df_valeurmoyenne = pd.DataFrame(data)

bar_chart = px.bar(df_valeurmoyenne, x='station', y='valeur_moyenne en ug.m-3')


# -- Traitements requis pour la carte :

# Création de la carte centrée sur Paris
map_global = folium.Map(location=(48.8534100,2.3488000), tiles='OpenStreetMap', zoom_start=11)
marker_cluster = MarkerCluster().add_to(map_global)

# création de la carte globale comportant tous les types d'arbre faite à part
for coor in df["fields.geo_point_2d"] :
    folium.Marker(location=[coor[0],coor[1]], fill_color='#43d9de', radius=8).add_to(marker_cluster)
# On ajoute les stations de relevé sur la carte
for station in data_json :
    if station != "_id" :
        lat = data_json[station]['Latitude']
        long = data_json[station]['Longitude']
        folium.Marker(location=[lat,long], popup=station, icon=folium.Icon(color="red", icon="info-sign")).add_to(map_global)
map_global.save(outfile='Global.html')

# Fonction permettant de générer une carte en fonction du type d'arbre choisi
def generate_map(type_arbre):
    # On créé une dataframe ne comportant que le type d'arbre choisi
    dataframe = df.set_index("fields.libellefrancais").loc[type_arbre].reset_index()
    # On créé la carte associée
    map = folium.Map(location=(48.8534100,2.3488000), tiles='OpenStreetMap', zoom_start=11)
    # On place les marqueurs sur la carte avec les coordonées de chaque arbre
    for coor in dataframe["fields.geo_point_2d"] :
        folium.Marker(location=[coor[0],coor[1]], fill_color='#43d9de', radius=8).add_to(map)
    # On place les marqueurs des stations de relevé de polluant
    for station in data_json :
        if station != "_id" :
            lat = data_json[station]['Latitude']
            long = data_json[station]['Longitude']
            folium.Marker(location=[lat,long], popup=station, icon=folium.Icon(color="red", icon="info-sign")).add_to(map)
    # On sauvegarde la carte dans un fichier html local
    file_name = type_arbre + '.html'
    map.save(outfile=file_name)


# -- Traitement pour le graphique des valeurs moyennes de polluant par mois pour une station donnée

# On fournit le nom de la station et le fichier json
def get_monthly_values(station,file):

    # On initialise nos variables
    dates = []
    value = []
    values = []
    current_month = (file[station]['Mesures'][0]['Mois'],file[station]['Mesures'][0]['Annee'])

    # Pour chaque relevé de mesures
    for  mesures in file[station]['Mesures'] :
        # On regarde si la mesure à été effectuée dans le mois
        if (mesures['Mois'] == current_month[0]) & (mesures['Annee'] == current_month[1]) :
            # Si c'est le cas, on ajoute la valeur et la date de la mesure à la lite
            date = datetime.datetime.strptime(mesures["Date"], '%Y-%m-%d %H:%M:%S').date()
            value.append(mesures["Valeur"])
        else :
            # Si ce n'est pas le cas, la mesure à été éffectuée dans un autre mois
            # On effectue alors la moyenne des mesures du mois précédent
            values.append(np.mean(value))
            dates.append(date)
            # On réinitialise nos variables au nouveau mois
            current_month = (mesures['Mois'],mesures['Annee'])
            value = []
            value.append(mesures["Valeur"])
    # On effectue la moyenne des mesures du dernier mois
    values.append(np.mean(value))
    dates.append(date)
    return(values,dates)

values,dates = get_monthly_values("PARIS stade Lenglen",data_json)
# création du dataframe pour le graphique
df_month_val = pd.DataFrame({'valeur moyenne de NO2 en ug.m-3' : values, 'date' : dates})
# création du graphique
monthly_val = px.line(df_month_val,x="date",y="valeur moyenne de NO2 en ug.m-3",title="Valeur moyenne de polluant par mois dans le 15E arrondissement")


# -- Traitement pour le nombre d'arbres plantés par mois pour un arrondissement donné

# On fournit le nom de l'arrondissement et le dataframe des arbres plantés dans Paris
def get_monthly_trees(Arrondissement,df):

    # Fonction permettant d'obtenir le prochain mois
    def get_next_month(date):
        date = datetime.datetime.strptime(date,'%Y-%m-%d')
        if date.month == 12:
            return str(datetime.date(date.year + 1, 1, 1))
        else:
            return str(datetime.date(date.year, date.month + 1, 1))

    # On réduit notre dataframe aux arbres plantés dans l'arrondissement concerné
    df_Arr = df.loc[df["fields.arrondissement"] == Arrondissement]
    # On définit la date de début d'étude 
    itrt = "2021-01-31"
    days = [itrt[:-3]]

    # Tant que la date (Année-mois) n'est pas comprise dans le mois actuel
    while itrt[:-3] != datetime.date.today().__format__('%Y-%m') :
        itrt = get_next_month(itrt)
        # On ajoute cette date dans une liste
        days.append(itrt[:-3])

    #Pour chaque arbre
    for index, row in df_Arr.iterrows() :
        #On extrait sa date de platation
        days.append(datetime.datetime.strptime(row['fields.dateplantation'], '%Y-%m-%dT%H:%M:%S+00:00').__format__('%Y-%m'))

    # On créé un dataframe avec les dates des arbres plantés et les dates depuis le début de l'étude afin de n'en manquer aucune
    # On compte ensuite le nombre d'arbres plantés par mois et on les classes dans l'ordre chronologique
    arbres_df = pd.Series(days).value_counts().sort_index(axis = 0, ascending = True).reset_index()
    # On convertie les dates au bon format
    arbres_df['index'] = arbres_df['index'].apply(lambda x : datetime.datetime.strptime(x,'%Y-%m'))
    # On réajuste les valeurs pour coller aux valeurs réelles
    arbres_df[0] = arbres_df[0] - 1
    # On met en forme notre dataframe
    arbres_df = arbres_df.rename(columns = {'index': 'date', 0 : 'nombre'})

    return(arbres_df)

Arrondissement = data_json['PARIS stade Lenglen']['Arr']
arbres_df = get_monthly_trees(Arrondissement,df)
# création du graphique
monthly_trees = px.bar(arbres_df,x="date",y="nombre",title="Nombre d'arbres plantés par mois dans le 15E arrondissement")


### Dashboard

app = Dash(__name__)


app.layout = html.Div([
    html.Button("Update datas in the database", id="btn_txt"), dcc.Location(id='update', refresh=True), #autorisations de refresh la page
    
    html.H1("Qualité de l'air à Paris", style={'textAlign': 'center', 'fontSize': 60}),

    #Valeurs en temps réel
    html.H2("Données de qualité de l'air en temps réel"),
    dash_table.DataTable(
        id='main_poll_table',
        columns=[{"name": i, "id": i} for i in main_poll_table.columns],
        data=main_poll_table.to_dict('records'),
    ),
    html.H2("Principaux polluants et leurs valeur en temps réel"),
    dash_table.DataTable(
        id='other_poll_table',
        columns=[{"name": i, "id": i} for i in other_poll_table.columns],
        data=other_poll_table.to_dict('records'),
    ),
    
    #Bar
    html.H2("Qualité moyenne de l'air depuis 2020"),
    dcc.Graph(
        id='bar',
        figure = bar_chart
    ), 

    #Map
    html.H2('Emplacement des arbres plantés selon leur type et position des stations de relevé'),
    dcc.Dropdown(
        id="tree-dropdown",
        options=[
            {'label':'Tous','value':'Global'},
            {'label':'Platanes','value':'Platane'},
            {'label':'Erables','value':'Erable'},
            {'label':'Sophora','value':'Sophora'},
            {'label':'Marronnier','value':'Marronnier'},
            {'label':'Tilleul','value':'Tilleul'}

        ],
        value = 'Global',
    ),  
    html.Iframe(id = 'Map', srcDoc = open('Global.html', 'r').read(), width = '100%', height = '600'),

    #Graphiques
    html.H2("Valeur moyenne de polluant par mois et nombre d'arbres plantés au même moment dans le 15E arrondissement"),
    dcc.Graph(
        id='monthly_val',
        figure = monthly_val
    ),
    html.H2(),
    dcc.Graph(
        id='monthly_trees',
        figure = monthly_trees
    ),

],style={'font-family':'Trebuchet MS, sans-serif','marginTop':'35px', 'width':'90%', 'margin': 'auto'})


# Callback pour le bouton
@app.callback(Output("update", "href"), Input("btn_txt", "n_clicks"))
# Fonction permettant d'update si click sur le bouton
# Refresh la page si les données sont mises à jour
def func(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        response_update = update_bdd()
        if response_update == 'UPDATE' :         
            print("update")
            return "/"
        else : 
            print("no update")
            return

@app.callback(
    Output('Map', 'srcDoc'),
    Input('tree-dropdown', 'value'))
def update_map(selected_tree):
    if(selected_tree == 'Global'):
        return open('Global.html','r').read()
    else :
        generate_map(selected_tree)
        map_name = selected_tree + '.html'
        return open(str(map_name),'r').read()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000, debug=True)
    # app.run_server(host='127.0.0.1', port=8000, debug=True)