import os

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
import plotly.plotly as py
from dash.dependencies import Input, Output, State


from src.components.dataPokemon import dfPokemon, dfPokemonTable
from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import listGoFunc, generateValuePlot, go #, generate_table

from src.components.tab1.callbacks import callbacksortingtable, callbackfiltertable

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
        dcc.Tab(label='Categorical Plots', value='tab-2', children=[
            html.Div([
                # DROP DOWN JENIS PLOT
                html.Div([
                    html.P('Jenis : '),
                    dcc.Dropdown(
                        id='jenisplotcategory',
                        options=[{'label': i, 'value': i} for i in ['Bar','Box','Violin']],
                        value='Bar'
                    )
                ], className='col-3'),
                # DROP DOWN X
                html.Div([
                    html.P('X : '),
                    dcc.Dropdown(
                        id='xplotcategory',
                        options=[{'label': i, 'value': i} for i in ['Generation','Type 1','Type 2']],
                        value='Generation'
                    )
                ], className='col-3'),
                # DROP DOWN Y
                html.Div([
                    html.P('Y : '),
                    dcc.Dropdown(
                        id='yplotcategory',
                        options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    )
                ], className='col-3'),
                # DROP DOWN LAST
                html.Div([
                    html.P('Stats : '),
                    dcc.Dropdown(
                        id='statsplotcategory',
                        options=[
                            i for i in [
                                {'label' : 'Mean', 'value' : 'mean'},
                                {'label' : 'Standard Deviation', 'value' : 'std'},
                                {'label' : 'Count', 'value' : 'count'},
                                {'label' : 'Min', 'value' : 'min'},
                                {'label' : 'Max', 'value' : 'max'},
                                {'label' : '25th Percentiles', 'value' : '25%'}, 
                                {'label' : 'Median', 'value' : '50%'},
                                {'label' : '75th Percentiles', 'value' : '75%'},
                            ]
                        ],
                        value='mean',
                        disabled = False
                    )
                ], className='col-3')
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='categoryGraph'
            )
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-3', children=[
            html.Div([
                # DROP DOWN SCATTER HUE PLOT
                html.Div([
                    html.P('Hue : '),
                    dcc.Dropdown(
                        id='hueplotscatter',
                        options=[{'label': i, 'value': i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    )
                ], className='col-4'),
                # DROP DOWN SCATTER X
                html.Div([
                    html.P('X : '),
                    dcc.Dropdown(
                        id='xplotscatter',
                        options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Attack'
                    )
                ], className='col-4'),
                # DROP DOWN SCATTER Y
                html.Div([
                    html.P('Y : '),
                    dcc.Dropdown(
                        id='yplotscatter',
                        options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='HP'
                    )
                ], className='col-4')
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='scatterGraph'
            )
        ]),
        dcc.Tab(label='Pie Chart', value='tab-4', children=[
            html.Div([
                # DROP DOWN PIE CHART GROUPING
                html.Div([
                    html.P('Group : '),
                    dcc.Dropdown(
                        id='groupplotpie',
                        options=[{'label': i, 'value': i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    )
                ], className='col-4')
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='pieGraph'
            )
        ]),
        dcc.Tab(label='Histogram', value='tab-5', children=[
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
            dcc.Graph(
                id='histGraph'
            )
        ])
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


# ________________CALLBACK TABLE________________

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

# ________________CALLBACK DISABLE STATS________________

@app.callback(
    Output(component_id='statsplotcategory', component_property='disabled'),
    [Input(component_id='jenisplotcategory', component_property='value')]
)

def update_disable_stats(jenisPlot):
    if (jenisPlot == 'Bar'):
        return False
    return True

# ________________CALLBACK SCATTER PLOT________________

# Buat nentuin legend name
legendScatterDict = {
    'Legendary' : {'True' : 'Non-Legendary', 'False' : 'Legendary'},
    'Generation' : { 1 : '1st Generation', 2 : '2nd Generation', 3 : '3rd Generation', 4 : '4th Generation', 5 : '5th Generation', 6 : '6th Generation'},
    'Type 1' : { i: i for i in dfPokemon['Type 1'].unique()},
    'Type 2' : { i: i for i in dfPokemon['Type 2'].unique()}
}

@app.callback(
    Output(component_id='scatterGraph', component_property='figure'),
    [Input(component_id='hueplotscatter', component_property='value'),
    Input(component_id='xplotscatter', component_property='value'),
    Input(component_id='yplotscatter', component_property='value')
    ]
)

def update_scatter_plot(hueScatter,xScatter,yScatter):
    return dict(
        data=[
            go.Scatter(
                x= dfPokemon[dfPokemon[hueScatter] == value][xScatter],
                y= dfPokemon[dfPokemon[hueScatter] == value][yScatter],
                name= legendScatterDict[hueScatter][value],
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

# # ________________CALLBACK PIE CHART________________

@app.callback(
    Output(component_id='pieGraph', component_property='figure'),
    [Input(component_id='groupplotpie', component_property='value')]
)

def update_pie_chart(group):
    return dict(
        data = [
            go.Pie(
                labels = [legendScatterDict[group][val] for val in dfPokemon[group].unique()],
                values = [len(dfPokemon[dfPokemon[group] == val]) for val in dfPokemon[group].unique()]
            ) 
        ],
        layout = go.Layout(
            title = 'Pie Chart Pokemon',
            margin = {'l' : 160, 'b' : 40, 't' : 40, 'r' : 20}
        )
    )

# ________________CALLBACK HISTOGRAM________________

rowcolhist = {
    'Generation' : {'row' : 3, 'col' : 2},
    'Legendary' : {'row' : 1, 'col' : 2}
}

@app.callback(
    Output(component_id='histGraph', component_property='figure'),
    [Input(component_id='histFilter', component_property='value'),
    Input(component_id='histHue', component_property='value'),
    Input(component_id='stdplothist', component_property='value')
    ]
)

def update_hist_plot(x, hue, std):
    std = int(std)
    if(hue == 'All') :
        return dict(
                data=[
                    go.Histogram(
                        x=dfPokemon[
                            (dfPokemon[x] >= (dfPokemon[x].mean() - (std * dfPokemon[x].std())))
                            & (dfPokemon[x] <= (dfPokemon[x].mean() + (std * dfPokemon[x].std())))
                        ][x],
                        name='Normal',
                        marker=dict(
                            color='green'
                        )
                    ),
                    go.Histogram(
                        x=dfPokemon[
                            (dfPokemon[x] < (dfPokemon[x].mean() - (std * dfPokemon[x].std())))
                            | (dfPokemon[x] > (dfPokemon[x].mean() + (std * dfPokemon[x].std())))
                        ][x],
                        name='Not Normal',
                        marker=dict(
                            color='red'
                        )
                    )
                ],
                layout=go.Layout(
                    title='Histogram {} Stats Pokemon'.format(x),
                    xaxis=dict(title=x),
                    yaxis=dict(title='Count'),
                    height=450, width=1000
                )
            )
    subtitles = []
    for val in dfPokemon[hue].unique() :
        dfSub = dfPokemon[dfPokemon[hue] == val]
        outlierCount = len(dfSub[
                        (dfSub[x] < (dfSub[x].mean() - (std * dfSub[x].std())))
                        | (dfSub[x] > (dfSub[x].mean() + (std * dfSub[x].std())))
                    ])
        subtitles.append(legendScatterDict[hue][val] + " ({}% outlier)".format(round(outlierCount/len(dfSub) * 100, 2)))

    fig = tools.make_subplots(
        rows=rowcolhist[hue]['row'], cols=rowcolhist[hue]['col'],
        subplot_titles=subtitles
    )
    uniqueData = dfPokemon[hue].unique().reshape(rowcolhist[hue]['row'],rowcolhist[hue]['col'])
    index=1
    for r in range(1, rowcolhist[hue]['row']+1) :
        for c in range(1, rowcolhist[hue]['col']+1) :
            dfSub = dfPokemon[dfPokemon[hue] == uniqueData[r-1,c-1]]
            fig.append_trace(
                go.Histogram(
                    x=dfSub[
                        (dfSub[x] >= (dfSub[x].mean() - (std * dfSub[x].std())))
                        & (dfSub[x] <= (dfSub[x].mean() + (std * dfSub[x].std())))
                    ][x],
                    name='Normal {} {}'.format(hue,uniqueData[r-1,c-1]),
                    marker=dict(
                        color='green'
                    )
                ),r,c
            )
            fig.append_trace(
                go.Histogram(
                    x=dfSub[
                        (dfSub[x] < (dfSub[x].mean() - (std * dfSub[x].std())))
                        | (dfSub[x] > (dfSub[x].mean() + (std * dfSub[x].std())))
                    ][x],
                    name='Not Normal {} {}'.format(hue, uniqueData[r-1,c-1]),
                    marker=dict(
                        color='red'
                    )
                ),r,c
            )
            fig['layout']['xaxis'+str(index)].update(title=x.capitalize())
            fig['layout']['yaxis'+str(index)].update(title='Count')
            index += 1

    if(hue == 'Generation') :
        fig['layout'].update(height=700, width=1000,
                            title='Histogram {} Stats Pokemon'.format(x))
    else :
        fig['layout'].update(height=450, width=1000,
                            title='Histogram {} Stats Pokemon'.format(x))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)  



