import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon

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

def callbackupdatecatgraph(jenisPlot,xPlot,yPlot,stats):
    return dict(
        layout= go.Layout(
            title = '{} Plot Pokemon'.format(jenisPlot),
            xaxis = {'title' : xPlot},
            yaxis = dict(title=yPlot),
            boxmode = 'group',
            violinmode = 'group',
        ),
        data = [
            listGoFunc[jenisPlot](
                x= generateValuePlot('True',xPlot,yPlot)['x'][jenisPlot],
                y= generateValuePlot('True',xPlot,yPlot,stats)['y'][jenisPlot],
                name = 'Legendary',
                opacity= 0.6
            ),
            listGoFunc[jenisPlot](
                x= generateValuePlot('False',xPlot,yPlot)['x'][jenisPlot],
                y= generateValuePlot('False',xPlot,yPlot,stats)['y'][jenisPlot],
                name = 'Non-Legendary',
                opacity= 0.6
            )
        ]
    )