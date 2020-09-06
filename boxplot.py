import random
from math import log, log10

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

print(pio.renderers.default)


def main():
    data = pd.read_csv("global_power_plant_database.csv")[[
        'country',
        'country_long',
        'primary_fuel',
        'capacity_mw'
    ]]

    power_plant_types = data.groupby(['primary_fuel'])['capacity_mw'].median().sort_values().axes[0]
    charts_orders = []
    fig = go.Figure()
    # pp = random.choice(power_plant_types)
    for pp in power_plant_types:
        fig.add_trace(go.Box(
            name=pp,
            y=data[pp == data['primary_fuel']]['capacity_mw'],
            visible=True
        ))
        charts_orders.append('World')

    for c in data['country_long'].unique():
        power_plant_types_in_c = \
        data[c == data['country_long']].groupby(['primary_fuel'])['capacity_mw'].median().sort_values().axes[0]
        for pp in power_plant_types_in_c:
            fig.add_trace(go.Box(
                name=pp,
                y=data[(pp == data['primary_fuel']) & (c == data['country_long'])]['capacity_mw'],
                visible=False,
                boxpoints="all"
            ))
            charts_orders.append(c)
    buttons = list([
        dict(label="World",
             method="update",
             args=[{"visible": [True if c == 'World' else False for c in charts_orders]}])

    ]
    )

    for country in data['country_long'].unique():
        buttons.append(
            dict(label=country,
                 method="update",
                 args=[{
                     "visible": [True if c == country else False for c in charts_orders]
                 }])
        )

    fig.update_layout(
        yaxis=dict(range=[log10(data['capacity_mw'].min() - 0.01), log10(int(data['capacity_mw'].max() * 1.25))]),
        yaxis_type="log",
        updatemenus=[
            dict(
                active=0,
                buttons=buttons
            )
        ]
    )

    fig.write_html('tmp.html', auto_open=True)


if __name__ == '__main__':
    main()
