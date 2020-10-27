from copy import deepcopy

import plotly
import plotly.graph_objects as go

from charts.carbon.carbon import carbon_data
from charts.geolocation.geolocation import join_on_iso_3, get_continents, continent_color


def shapes(x0, x1, color):
    return dict(
        type="rect",
        xref="x",
        yref="paper",
        x0=x0,
        y0=0,
        x1=x1,
        y1=1,
        fillcolor=color,
        opacity=0.5,
        layer="below",
        line_width=0
    )


def scatter_fig(data, continent):
    aux_data = deepcopy(data)
    aux_data = aux_data[(aux_data['Continent'] == continent) & (aux_data['Annual CO2 emissions (tonnes)'] > 0)]
    return {
        'x': aux_data['Year'],
        'y': aux_data['Annual CO2 emissions (tonnes)'],
        'name': continent,
        'mode': 'lines',
        'legendgroup': "group",
        'line_color': continent_color(continent)
    }


def timeline():
    co = carbon_data().dropna()
    co = join_on_iso_3(co, 'Code')
    co = co.groupby(['Continent', 'Year']).sum().reset_index()
    important_year = [
        [1914, 1918, "#C0BCB5"],
        [1929, 1933, "#4A6C6F"],
        [1939, 1945, "#846075"],
        [1956, 1960, "#AF5D63"],
        [1989, 1992, "#ED474A"],
        [2008, 2010, "#9649CB"]
    ]
    fig = go.Figure()
    for c in get_continents():
        fig.add_trace(go.Scatter(**scatter_fig(co, c)))

    fig.update_yaxes(range=[0, 22 * 10 ** 9])
    fig.update_layout(
        xaxis=dict(
            autorange=True,
            rangeslider=dict(
                autorange=True)
        ),
        shapes=[shapes(*years) for years in important_year]
    )
    # fig.write_html('tmp3.html', auto_open=True)
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


if __name__ == '__main__':
    timeline()
