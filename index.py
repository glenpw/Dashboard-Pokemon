import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from src.components.dataPokemon import dfPokemon, dfPokemonTable
from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import renderIsiTab2
from src.components.tab3.view import renderIsiTab3
from src.components.tab4.view import renderIsiTab4
from src.components.tab5.view import renderIsiTab5
from src.components.tab6.view import renderIsiTab6
from src.components.tab7.view import renderIsiTab7

from src.components.tab1.callbacks import callbacksortingtable, callbackfiltertable
from src.components.tab2.callbacks import callbackupdatecatgraph
from src.components.tab3.callbacks import callbackupdatescattergraph
from src.components.tab4.callbacks import callbackupdatepiechart
from src.components.tab5.callbacks import callbackupdatehistogram
from src.components.tab6.callbacks import callbackpredict
from src.components.tab7.callbacks import callbacksortingtablehistory, callbackfiltertablehistory

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# dfPokemon = pd.read_csv('PokemonKece.csv')

app = dash.Dash(__name__) # external_stylesheets=external_stylesheets)
server = app.server

app.title = 'Dashboard Pokemon'

app.layout = html.Div([
    html.H1('Dashboard Pokemon',style={'color': '#000080'}),
    html.H4('Created by Glen P. Wangsa'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Pokemon', value='tab-1', children=renderIsiTab1()),
        dcc.Tab(label='Categorical Plots', value='tab-2', children=renderIsiTab2()),
        dcc.Tab(label='Scatter Plot', value='tab-3', children=renderIsiTab3()),
        dcc.Tab(label='Pie Chart', value='tab-4', children=renderIsiTab4()),
        dcc.Tab(label='Histogram', value='tab-5', children=renderIsiTab5()),
        dcc.Tab(label='Test Predict', value='tab-6', children=renderIsiTab6()),
        dcc.Tab(label='History Prediction', value='tab-7', children=renderIsiTab7())
    ],
    style={'fontFamily': 'Arial'},
    content_style={
        'fontFamily' : 'system-ui',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '50px'
    })],
    style={
        'maxWidth' : '1200px',
        'margin' : '0 auto'
    }
)

# ______________CALLBACK TABLE________________
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_sort_paging_table(pagination_settings, sorting_settings):
    return callbacksortingtable(pagination_settings, sorting_settings)

@app.callback(
    Output(component_id='tableData', component_property='children'),
    [Input(component_id='buttonsearch', component_property='n_clicks'),
    Input(component_id='rowMax', component_property='value')],
    [State(component_id='nameSearch', component_property='value'),
    State(component_id='legendSearch', component_property='value'),
    State(component_id='genSearch', component_property='value'),
    State(component_id='totalSearch', component_property='value')]
)
def update_table(n_clicks,maxrows,name,legend,gen,total):
    return callbackfiltertable(n_clicks,maxrows,name,legend,gen,total)

# ________________CALLBACK PLOT________________
@app.callback(
    Output(component_id='categoryGraph', component_property='figure'),
    [
        Input(component_id='jenisplotcategory', component_property='value'),
        Input(component_id='xplotcategory', component_property='value'),
        Input(component_id='yplotcategory', component_property='value'),
        Input(component_id='statsplotcategory', component_property='value')
    ]
)
def update_category_graph(jenisPlot,xPlot,yPlot,stats):
    return callbackupdatecatgraph(jenisPlot,xPlot,yPlot,stats)

# __________CALLBACK DISABLE STATS_____________
@app.callback(
    Output(component_id='statsplotcategory', component_property='disabled'),
    [Input(component_id='jenisplotcategory', component_property='value')]
)
def update_disable_stats(jenisPlot):
    if (jenisPlot == 'Bar'):
        return False
    return True

# ___________CALLBACK SCATTER PLOT_____________
@app.callback(
    Output(component_id='scatterGraph', component_property='figure'),
    [Input(component_id='hueplotscatter', component_property='value'),
    Input(component_id='xplotscatter', component_property='value'),
    Input(component_id='yplotscatter', component_property='value')
    ]
)
def update_scatter_plot(hueScatter,xScatter,yScatter):
    return callbackupdatescattergraph(hueScatter,xScatter,yScatter)

# ________________CALLBACK PIE CHART________________
@app.callback(
    Output(component_id='pieGraph', component_property='figure'),
    [Input(component_id='groupplotpie', component_property='value')]
)
def update_pie_chart(group):
    return callbackupdatepiechart(group)

# ________________CALLBACK HISTOGRAM________________
@app.callback(
    Output(component_id='histGraph', component_property='figure'),
    [Input(component_id='histFilter', component_property='value'),
    Input(component_id='histHue', component_property='value'),
    Input(component_id='stdplothist', component_property='value')
    ]
)
def update_hist_plot(x, hue, std):
    return callbackupdatehistogram(x, hue, std)

# ______________CALLBACK PREDICT________________
@app.callback(
    Output(component_id='outputpredict', component_property='children'),
    [Input(component_id='buttonpredict', component_property='n_clicks')],
    [State(component_id='predictname', component_property='value'),
    State(component_id='predicttype1', component_property='value'),
    State(component_id='predicttype2', component_property='value'),
    State(component_id='predictgen', component_property='value'),
    State(component_id='predicttotal', component_property='value'),
    State(component_id='predicthp', component_property='value'),
    State(component_id='predictattack', component_property='value'),
    State(component_id='predictdefense', component_property='value'),
    State(component_id='predictspattack', component_property='value'),
    State(component_id='predictspdef', component_property='value'),
    State(component_id='predictspeed', component_property='value')
    ]
)
def update_predict(n_clicks,name,type1,type2,gen,total,hp,attack,defense,spatk,spdef,speed):
    return callbackpredict(n_clicks,name,type1,type2,gen,total,hp,attack,defense,spatk,spdef,speed)

# ______________CALLBACK TABLE HISTORY________________
@app.callback(
    Output('table-history-prediction', "data"),
    [Input('table-history-prediction', "pagination_settings"),
     Input('table-history-prediction', "sorting_settings")])
def update_sort_paging_table_history(pagination_settings, sorting_settings):
    return callbacksortingtablehistory(pagination_settings, sorting_settings)

@app.callback(
    Output(component_id='tablehistorydiv', component_property='children'),
    [Input(component_id='filtercreatedbyhistory', component_property='value'),
    Input(component_id='filterrowhistory', component_property='value')
    ]
)
def update_table_history(createdby, maxrows):
    return callbackfiltertablehistory(createdby, maxrows)

if __name__ == '__main__':
    app.run_server(debug=True)  