import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon
from src.components.support import legendDict

def callbackupdatescattergraph(hueScatter,xScatter,yScatter):
    return dict(
        data=[
            go.Scatter(
                x= dfPokemon[dfPokemon[hueScatter] == value][xScatter],
                y= dfPokemon[dfPokemon[hueScatter] == value][yScatter],
                name= legendDict[hueScatter][value],
                mode= 'markers'
            ) for value in dfPokemon[hueScatter].unique()
        ],
        layout= go.Layout(
            title = 'Scatter Plot Pokemon',
            xaxis = {'title' : 'Attack'},
            yaxis = {'title' : 'HP'},
            hovermode = 'closest',
            margin = {'l' : 40, 'b' : 40, 't' : 40, 'r' : 20}
        )
    )