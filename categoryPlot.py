import plotly.graph_objs as go
import pandas as pd
import requests
import dash_core_components as dcc
import dash_html_components as html

res = requests.get('http://api-pokemon-baron.herokuapp.com/pokemon')
dfPokemon = pd.DataFrame(res.json(), columns=res.json()[0].keys())

listGoFunc = {
    'Bar' : go.Bar,
    'Box' : go.Box,
    'Violin' : go.Violin
}

def generateValuePlot(legendary,x,y,stats = 'mean'):
    return {
        'x' : {
            'Bar' : dfPokemon[dfPokemon['Legendary'] == legendary][x].unique(),
            'Box' : dfPokemon[dfPokemon['Legendary'] == legendary][x],
            'Violin' : dfPokemon[dfPokemon['Legendary'] == legendary][x],
        },
        'y' : {
            'Bar' : dfPokemon[dfPokemon['Legendary'] == legendary].groupby(x)[y].describe()[stats],
            'Box' : dfPokemon[dfPokemon['Legendary'] == legendary][y],
            'Violin' : dfPokemon[dfPokemon['Legendary'] == legendary][y],
        }
    }

def generate_table(dataframe, max_row=10):
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        #Body
        [html.Tr(
            [html.Td(
                str(dataframe.iloc[i][col])) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), int(max_row)))]
    )