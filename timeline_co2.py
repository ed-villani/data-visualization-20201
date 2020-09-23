import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    co = pd.read_csv("annual-co-emissions-by-region.csv")
    co = co.dropna()
    country_continent = pd.read_excel("country_continent.xlsx")
    country_continent.loc[country_continent['Region'] == 'North America', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'Central America', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'West Indies', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'South America', 'Continent'] = 'South America'
    co = co.join(country_continent.set_index('ISO (3)'), on='Code')

    co = co.groupby(['Continent', 'Year']).sum().reset_index()
    co_per_continent = co
    co_per_continent = co_per_continent[co_per_continent['Year'] == 2018].sort_values(
        by=['Annual CO2 emissions (tonnes)'], ascending=True)

    continent_list = co_per_continent['Continent'].to_list()
    colors = [
        '#003f5c',
        '#444e86',
        '#955196',
        '#dd5182',
        '#ff6e54',
        '#ffa600'
    ]


    fig = go.Figure()
    for c, color in zip(continent_list, colors):
        data = co[(co['Continent'] == c) & (co['Annual CO2 emissions (tonnes)'] > 0)]
        fig.add_trace(go.Scatter(x=data['Year'], y=data['Annual CO2 emissions (tonnes)'],
                                 name=c,
                                 mode='lines',
                                 legendgroup="group",
                                 line_color=color
                                 ))
    fig.update_yaxes(range=[0, 22 * 10 ** 9])
    fig.update_layout(
        xaxis=dict(
            autorange=True,
            rangeslider=dict(
                autorange=True)
        ),
        shapes=[
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=1914,
                y0=0,
                x1=1918,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            ),
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=1939,
                y0=0,
                x1=1945,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            ),
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=2008,
                y0=0,
                x1=2009,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            ),
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=1929,
                y0=0,
                x1=1933,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            ),
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=1989,
                y0=0,
                x1=1992,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            ),
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=1956,
                y0=0,
                x1=1960,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
            )
        ]
    )
    fig.write_html('tmp3.html', auto_open=True)


if __name__ == '__main__':
    main()
