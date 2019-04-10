import dash_html_components as html
import dash_core_components as dcc
from src.components.dataPokemon import dfPokemon

def renderIsiTab5():
    return [
            html.Div([
                html.Div([
                    html.P('Filter X : '),
                    dcc.Dropdown(
                        id='histFilter',
                        options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Hue : '),
                    dcc.Dropdown(
                        id='histHue',
                        options=[{'label': i, 'value': i} for i in ['All','Legendary','Generation']],
                        value='All'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Standard Deviation : '),
                    dcc.Dropdown(
                        id='stdplothist',
                        options=[{'label': '{} STD'.format(i), 'value': i} for i in ['1','2','3']],
                        value='2'
                    )
                ], className='col-3')  
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='histGraph'
            )
        ]