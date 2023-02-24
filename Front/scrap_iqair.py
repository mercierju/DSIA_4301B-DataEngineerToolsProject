import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_tables() :

    # On récupère la page internet à scrapper
    response = requests.get("https://www.iqair.com/fr/france/ile-de-france/paris")
    soup = BeautifulSoup(response.text,features="lxml")

    # On récupère les deux tableaux qui nous intéressent sur cette page
    table_indice = soup.find('table', class_="aqi-overview-detail__main-pollution-table")
    table_indice2 = soup.find('table', class_="aqi-overview-detail__other-pollution-table")

    # On récuppère les valeurs du tableau
    def scrap_table(table_indice):
        header = []
        rows = []
        for i, row in enumerate(table_indice.find_all('tr')):
            if i == 0:
                header = [el.text.strip() for el in row.find_all('th')]
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])
        rows.insert(0,header)
        return rows

    # On récupère le premier tableau sous forme de dataframe
    rows0 = scrap_table(table_indice)
    main_poll_table = pd.DataFrame(data=rows0[1:],columns=rows0[0])

    # On fait de même pour le deuxième tableau
    rows1 = scrap_table(table_indice2)
    for row in rows1[1:]:
        row.pop(1)
    other_poll_table = pd.DataFrame(data=rows1[1:],columns=rows1[0])

    return main_poll_table,other_poll_table