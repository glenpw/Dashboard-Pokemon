import dash_html_components as html
import dash_core_components as dcc
from src.components.dataPokemon import dfPokemon

def renderIsiTab6():
    return [
        html.H3('Predict New Pokemon',className='title',style={'text-align':'center'}),
        html.Div([
            html.Div([
                html.P('Name : '),
                dcc.Input(id='predictname', type='text', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('Type 1 : '),
                dcc.Dropdown(
                    id='predicttype1',
                    options=[{'label': i, 'value': i} for i in sorted(dfPokemon['Type 1'].unique())],
                    value=''
                )
            ], className='col-3'),
            html.Div([
                html.P('Type 2 : '),
                dcc.Dropdown(
                    id='predicttype2',
                    options=[{'label': i, 'value': i} for i in sorted(dfPokemon['Type 2'].unique())],
                    value=''
                )
            ], className='col-3'),
                html.Div([
                html.P('Generation : '),
                dcc.Dropdown(
                    id='predictgen',
                    options=[{'label': i, 'value': i} for i in ['1','2','3','4','5','6']],
                    value=''
                )
            ], className='col-3')
        ], className='row paddingtop'),
        html.Div([
            html.Div([
                html.P('Total : '),
                dcc.Input(id='predicttotal', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('HP : '),
                dcc.Input(id='predicthp', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('Attack : '),
                dcc.Input(id='predictattack', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('Defense : '),
                dcc.Input(id='predictdefense', type='number', value='',style=dict(width='100%'))
            ], className='col-3')
        ], className='row paddingtop'),
        html.Div([
            html.Div([
                html.P('Sp. Attack : '),
                dcc.Input(id='predictspattack', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('Sp. Defense : '),
                dcc.Input(id='predictspdef', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.P('Speed : '),
                dcc.Input(id='predictspeed', type='number', value='',style=dict(width='100%'))
            ], className='col-3'),
            html.Div([
                html.Button('Predict', id='buttonpredict', style=dict(width='100%',marginTop='31px'))
            ], className='col-3'),
        ], className='row paddingtop'),
        html.Center([
            html.H3('', id='outputpredict')
        ])
    ]