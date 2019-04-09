import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon
from src.components.support import legendDict

def callbackupdatepiechart(group):
    return dict(
        data = [
            go.Pie(
                labels = [legendDict[group][val] for val in dfPokemon[group].unique()],
                values = [len(dfPokemon[dfPokemon[group] == val]) for val in dfPokemon[group].unique()]
            ) 
        ],
        layout = go.Layout(
            title = 'Pie Chart Pokemon',
            margin = {'l' : 160, 'b' : 40, 't' : 40, 'r' : 20}
        )
    )