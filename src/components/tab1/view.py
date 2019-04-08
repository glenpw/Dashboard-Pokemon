import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from src.components.dataPokemon import dfPokemon, dfPokemonTable

# def generate_table(dataframe, max_row=10):
#     return html.Table(
#         #Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#         #Body
#         [html.Tr(
#             [html.Td(
#                 str(dataframe.iloc[i][col])) for col in dataframe.columns
#                 ]) for i in range(min(len(dataframe), int(max_row)))]
#     )

def generate_table(dataframe, pagesize=10):
    return dt.DataTable(
        id='table-multicol-sorting',
        columns=[
            {"name": i, "id": i} for i in dataframe.columns
        ],
        pagination_settings={
            'current_page': 0,
            'page_size': pagesize
        },
        style_table={'overflowX': 'scroll'},
        pagination_mode='be',
        sorting='be',
        sorting_type='multi',
        sorting_settings=[]
    )

def renderIsiTab1():
    return [
            html.Div([
                html.Div([
                    html.P('Name : '),
                    dcc.Input(id='nameSearch', type='text', value='',style=dict(width='100%'))
                ], className='col-4'),
                html.Div([
                    html.P('Legendary : '),
                    dcc.Dropdown(
                        id='legendSearch',
                        options=[{'label': i, 'value': i} for i in ['All','False','True']],
                        value='All'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Generation : '),
                    dcc.Dropdown(
                        id='genSearch',
                        options=[{'label': i, 'value': i} for i in ['All','1','2','3','4','5','6']],
                        value='All'
                    )
                ], className='col-4')
            ], className='row'),html.Br(),
            html.Div([
                html.Div([
                    html.P('Total : '),
                    dcc.RangeSlider(
                        marks={i: str(i) for i in range(dfPokemon['Total'].min(), dfPokemon['Total'].max()+1, 60)},
                        min=dfPokemon['Total'].min(),
                        max=dfPokemon['Total'].max(),
                        value=[dfPokemon['Total'].min(),dfPokemon['Total'].max()],
                        className='rangeslider',
                        id='totalSearch'
                    ),
                ], className='col-10'),
                    html.Div([
                        html.Br(),
                        html.Button('Search', id='buttonsearch', style=dict(width='100%'))
                    ], className='col-2'),
            ], className = 'row'),html.Br(),html.Br(),
            html.Div([
                html.P('Max Row : '),
                dcc.Input(id='rowMax', value=10, type='number', max=len(dfPokemonTable))
            ], className='col-'),
            html.Center([
                html.H2('Data Pokemon', className='title')      
            ]),
            html.Center(id='tableData', children=generate_table(dfPokemonTable))
        ]