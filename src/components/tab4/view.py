import dash_html_components as html
import dash_core_components as dcc

def renderIsiTab4():
    return [
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
        ]