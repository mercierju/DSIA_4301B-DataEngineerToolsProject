import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly_express as px
import requests
import dash
from dash.dependencies import Output, Input
import numpy as np


#Récupération des données par le front

air_quality_datas = requests.get('http://back:5000/get_air_quality_datas')
# air_quality_datas = requests.get('http://localhost:5000/get_air_quality_datas')
data_json = air_quality_datas.json()



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



app = Dash(__name__)


app.layout = html.Div([
    html.Button("Update datas in the database", id="btn_txt"), dcc.Location(id='update', refresh=True), #autorisations de refresh la page
    
    html.H1("Qualité de l'air à Paris", style={'textAlign': 'center', 'fontSize': 60}),


    #Bar
    html.H2("Qualité moyenne de l'air depuis 2020"),
    dcc.Graph(
        id='bar',
        figure = bar_chart
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





if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000, debug=True)
    # app.run_server(host='127.0.0.1', port=8000, debug=True)