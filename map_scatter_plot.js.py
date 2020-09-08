

import pandas as pd
import plotly.graph_objects as go
import numpy as np

def main():
    data = pd.read_csv("global_power_plant_database.csv")
    regions = pd.read_excel("contry_continent.xlsx")
    data = data.join(regions.set_index('ISO (3)'), on='country')
    # data = data[data['primary_fuel'] == "Nuclear"]
    # regions.loc[regions['Region'] == 'South Asia', 'Continent'] = 'Asia'
    # regions.loc[regions['Region'] == 'South Asia', 'Continent'] = 'Asia'
    data.sort_values('capacity_mw', ascending=False)

    data['text'] = data['name'] + "<br>" + data['capacity_mw'].astype(str) + " Mw"
    power_plant_types = data.groupby(['primary_fuel'])['capacity_mw'].median().sort_values().axes[0]
    charts_orders = []
    fig = go.Figure()
    for pp in power_plant_types:
        df_sub = data[pp == data['primary_fuel']]
        fig.add_trace(go.Scattergeo(
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            text=df_sub['text'],
            mode='markers',
            marker=dict(
                size=df_sub['capacity_mw'],
                sizemode='area'
            ),
            visible=True if pp == power_plant_types[0] else False
        ))
        charts_orders.append(pp)

    buttons = list()

    for pp in power_plant_types:
        buttons.append(
            dict(label=pp,
                 method="update",
                 args=[{
                     "visible": [True if pp == p else False for p in charts_orders]
                 }])
        )

    fig.update_layout(
        title='Most trafficked US airports<br>(Hover for airport names)',
        updatemenus=[
            dict(
                active=0,
                buttons=buttons
            )
        ]
    )
    fig.write_html('tmp1.html', auto_open=True)


if __name__ == '__main__':
    main()
