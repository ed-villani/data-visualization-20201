from copy import deepcopy

import plotly.graph_objects as go
import plotly

from charts.geolocation.geolocation import join_on_iso_3
from charts.power_plants.power_plants import get_power_plants_types, get_data_by_primary_fuel, set_visible_by_option, \
    read_power_plants


def map_scatter_plot():
    data = read_power_plants()
    power_plant_types = get_power_plants_types(data)
    data = join_on_iso_3(data, 'country')
    limits = [
        [1, 99],
        [100, 999],
        [1000, 9999],
        [10000, 99999]
    ]

    data.sort_values('capacity_mw', ascending=False)
    data = set_new_limits(data)
    data = set_text_for_map_plot(data)

    fig = go.Figure()
    charts, charts_orders = set_charts(data, limits, power_plant_types)
    for c in charts:
        fig.add_trace(c)

    buttons = [
        dict(
            label=pp,
            method="update",
            args=[
                {
                    "visible": set_visible_by_option(pp, charts_orders)
                },
                {
                    "title": f'Locations of {pp} Power Plants  in the World<br>(Hover Power Plant for Details)'
                }
            ]) for pp in power_plant_types
    ]

    fig.update_layout(
        title=f'Locations of {power_plant_types[0]} Power Plants  in the World<br>(Hover Power Plant for Details)',
        updatemenus=[
            dict(
                active=0,
                buttons=buttons
            )
        ]
    )
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


def set_charts(data, limits, power_plant_types):
    charts = [
        go.Scattergeo(
            **set_scatter_map_data(
                get_data_by_capacity_limits(get_data_by_primary_fuel(data, pp), limit),
                limit,
                pp,
                power_plant_types[0]
            )
        ) for pp in power_plant_types for limit in limits
    ]
    charts_orders = [
        pp for pp in power_plant_types for _ in limits
    ]
    return charts, charts_orders


def get_data_by_capacity_limits(data, limit):
    aux_data = deepcopy(data)
    return aux_data[(aux_data['capacity_mw'] > limit[0]) & (aux_data['capacity_mw'] <= limit[1])]


def set_text_for_map_plot(data):
    aux_data = deepcopy(data)
    aux_data['text'] = aux_data['name'] + "<br>" + aux_data['capacity_mw'].astype(str) + " Mw<br>" + aux_data[
        'country_long']
    return aux_data


def set_new_limits(data):
    aux_data = deepcopy(data)
    aux_data['aux_capacity_mw'] = aux_data['capacity_mw']
    aux_data.loc[aux_data['capacity_mw'] < 100, 'aux_capacity_mw'] = 400
    aux_data.loc[(aux_data['capacity_mw'] > 99) & (aux_data['capacity_mw'] < 1000), 'aux_capacity_mw'] = 900
    aux_data.loc[(aux_data['capacity_mw'] > 999) & (4999 > aux_data['capacity_mw']), 'aux_capacity_mw'] = 2500
    aux_data.loc[(aux_data['capacity_mw'] > 5000) & (100000 > aux_data['capacity_mw']), 'aux_capacity_mw'] = 12000
    return aux_data


def set_scatter_map_data(data, limit, power_plant_type, default_power_plant, scale_factor=50):
    return {
        "lon": data['longitude'],
        "lat": data['latitude'],
        "text": data['text'],
        "mode": 'markers',
        "marker": dict(
            size=data['aux_capacity_mw'] / scale_factor,
            sizemode="area"
        ),
        "name": f'{limit[0]} - {limit[1]} MW',
        "visible": True if power_plant_type == default_power_plant else False
    }