from copy import deepcopy
from math import log10

import pandas as pd
import plotly.graph_objects as go

from charts.power_plants.power_plant_colors import get_power_plant_color

GLOBAL_POWER_PLANT_DB = '/Users/eduardovillani/git/data-visualization-20201/data/power_plants/global_power_plant_database.csv'


def main():
    data = pd.read_csv(GLOBAL_POWER_PLANT_DB)[[
        'country',
        'country_long',
        'primary_fuel',
        'capacity_mw'
    ]]

    countries_names = get_country_names(data)
    buttons = []
    charts_orders = []

    fig = go.Figure()
    for c in countries_names:
        power_plant_types_in_c = get_power_plants_types(data, c)
        for pp in power_plant_types_in_c:
            fig.add_trace(go.Box(
                name=pp,
                y=capacity_per_power_plant(data, pp, c),
                visible=False if c != 'World' else True,
                boxpoints="all" if c != 'World' else None,
                marker_color=get_power_plant_color(pp)
            ))
            charts_orders.append(c)

    for c in countries_names:
        buttons.append(
            dict(
                label=c,
                method="update",
                args=[
                    {
                        "visible": set_visible_by_country_option(c, charts_orders)
                    }
                ]
            )
        )

    fig.update_layout(
        yaxis=dict(range=[log10(data['capacity_mw'].min() - 0.01), log10(int(data['capacity_mw'].max() * 1.25))]),
        yaxis_type="log",
        updatemenus=[
            dict(
                active=0,
                buttons=buttons
            )
        ],
        title={
            'text': "Power Plant Capacity (MW) by type<br>(For Countries, every point is a power plant)",
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Capacity (MW)",
        xaxis_title="Power Plant Type"
    )

    fig.write_html('tmp.html', auto_open=True)


def get_country_names(data):
    return ['World'] + data['country_long'].unique().tolist()


def capacity_per_power_plant(data, power_plant_type, country='World'):
    """
    Returns the power plants capacity
    :param power_plant_type:
    :param country:
    :param data:
    :return: power_pant_types
    """
    aux_data = deepcopy(data)
    if country == 'World':
        capacity = aux_data[power_plant_type == aux_data['primary_fuel']]['capacity_mw']
    else:
        capacity = aux_data[(power_plant_type == aux_data['primary_fuel']) & (country == aux_data['country_long'])][
            'capacity_mw']
    del aux_data
    return capacity


def get_power_plants_types(data, country='World'):
    """
    Returns the power plants type for the data file sorted by the world median of capacity
    :param country:
    :param data:
    :return: power_pant_types
    """
    aux_data = deepcopy(data)
    if country == 'World':
        power_plant_types = aux_data
    else:
        power_plant_types = aux_data[country == aux_data['country_long']]
    del aux_data
    return power_plant_types.groupby(['primary_fuel'])['capacity_mw'].median().sort_values().axes[0]


def set_visible_by_country_option(country, country_list):
    return [True if c == country else False for c in country_list]


if __name__ == '__main__':
    main()
