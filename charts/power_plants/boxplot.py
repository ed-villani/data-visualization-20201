from copy import deepcopy
from math import log10

import plotly
import plotly.graph_objects as go

from charts.power_plants.power_plant_colors import get_power_plant_color
from charts.power_plants.power_plants import get_power_plants_types, set_visible_by_option, read_power_plants


def chart_boxplot():
    data = read_power_plants()

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
                        "visible": set_visible_by_option(c, charts_orders)
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

    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


def get_country_names(data, world=True):
    """
    Return World's Countries list
    :param data:
    :param world:
    :return:
    """
    if world:
        return ['World'] + data['country_long'].unique().tolist()
    else:
        return data['country_long'].unique().tolist()


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


if __name__ == '__main__':
    main()
