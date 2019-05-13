import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from src.components.dataPokemon import dfHistoryTable

def generate_table(dataframe, pagesize=10):
    return dt.DataTable(
        id='table-history-prediction',
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

def renderIsiTab7():
    return [
            html.Div([
                html.Div([
                    html.P('Created By : '),
                    dcc.Input(id='filtercreatedbyhistory', type='text', value='',style=dict(width='100%'))
                ], className='col-4'),
            ], className='row'),html.Br(),
            html.Div([
                html.Div([
                    html.P('Max Row : '),
                    dcc.Input(id='filterrowhistory', value=10, type='number', style=dict(width='100%'))
                ], className='col-2'),
            ], className='row'),
            html.Center(html.H2('History Prediction', className='title')),
            html.Center(id='tablehistorydiv', children=generate_table(dfHistoryTable))
        ]