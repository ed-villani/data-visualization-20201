import plotly
import plotly.graph_objects as go

from charts.build_hierarchical_dataframe import build_hierarchical_dataframe
from charts.geolocation.geolocation import continent_color, get_continents
from charts.power_plants.power_plants import total_capacity_per_country


def fig_treemap(data):
    return {
        'labels': data['id'],
        'parents': data['parent'],
        'values': data['value'],
        'branchvalues': 'total',
        'textinfo': "label+value+percent parent+percent entry+percent root",
        'hovertemplate': '<b>%{label}</b><br> Capacity: %{value} MW',
        'name': ''
    }


def treemap_capacity():
    levels = ['Country', 'Region', 'Continent']
    color_columns = ['capacity_mw', 'quantity']
    value_column = 'capacity_mw'
    df = total_capacity_per_country()
    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    fig = go.Figure()
    fig.add_trace(go.Treemap(**fig_treemap(df_all_trees)))
    fig.update_layout(
        title={
            'text': "Conutries Capacity (MW) Proportional to Numbers of Power Plant <br>(Hoover for more information)",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        treemapcolorway=[continent_color(c) for c in get_continents()],
    )
    # fig.write_html('tmp3.html', auto_open=True)
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


if __name__ == '__main__':
    treemap_capacity()
