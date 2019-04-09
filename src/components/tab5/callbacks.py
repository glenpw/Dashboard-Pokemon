import plotly.graph_objs as go
from plotly import tools

from src.components.dataPokemon import dfPokemon
from src.components.support import legendDict


rowcolhist = {
    'Generation' : {'row' : 3, 'col' : 2},
    'Legendary' : {'row' : 1, 'col' : 2}
}

def callbackupdatehistogram(x, hue, std):
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
        subtitles.append(legendDict[hue][val] + " ({}% outlier)".format(round(outlierCount/len(dfSub) * 100, 2)))

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