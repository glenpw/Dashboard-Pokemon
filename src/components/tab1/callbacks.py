import requests
import pandas as pd

from src.components.tab1.view import generate_table
from src.components.dataPokemon import dfPokemonTable

def callbacksortingtable(pagination_settings, sorting_settings):
    # print(sorting_settings)
    if len(sorting_settings):
        dff = dfPokemonTable.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = dfPokemonTable

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

def callbackfiltertable(n_clicks,maxrows,name,legend,gen,total):
    global dfPokemonTable
    urlget = 'http://api-pokemon-baron.herokuapp.com/pokemon?name={}&mintotal={}&maxtotal={}'.format(name,total[0],total[1])
    if(gen != 'All'):
        urlget += '&generation={}'.format(gen)
    if(legend != 'All'):
        urlget += '&legendary={}'.format(legend)

    res = requests.get(urlget)
    dfPokemonTable = pd.DataFrame(res.json(), columns=res.json()[0].keys()) 

    return generate_table(dfPokemonTable, pagesize=int(maxrows))

    # dfFilter = dfPokemon[((dfPokemon['Total'] >= total[0]) & (dfPokemon['Total'] <= total[1]))]
    # if(name == ''):
    #     df1 = dfFilter 
    # else:
    #     df1 = dfFilter[dfFilter['Name'].str.contains(name)]
    # if(legend == 'All'):
    #     df2 = df1
    # elif(len(legend) > 3):
    #     df2 = df1[df1['Legendary'] == legend]
    # if(gen == 'All'):
    #     df3 = df2   
    # else:
    #     df3 = df2[df2['Generation'] == int(gen)]
    # return generate_table(df3, pagesize=max_rows)