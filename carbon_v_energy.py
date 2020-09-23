from copy import deepcopy
from math import log10

import pandas as pd
import plotly.graph_objects as go

from timeline_co2_and_timeline_power import county_continent


def pop_per_year():
    pop_per_year = pd.read_excel("pop_per_year_per_country.xls")
    pop_per_year = pop_per_year[['Country Name', 'Country Code'] + [str(i) for i in range(1960, 2019)]]
    country_continent = county_continent()
    pop_per_year = pop_per_year.join(country_continent.set_index('ISO (3)'), on='Country Code')
    return deepcopy(pop_per_year)[['Country Name'] + [str(i) for i in range(1960, 2019)]].set_index('Country Name').T.reset_index()


def main():
    pop = pop_per_year()
    co = pd.read_csv("annual-co-emissions-by-region.csv").dropna()
    data = co[(co['Entity'] == 'Argentina') & (co['Year'] > 1971)]
    data = data.reset_index()['Annual CO2 emissions (tonnes)']

    energy = pd.read_excel(
        'World_Energy_Balances_Highlights_(2020_edition).xlsx',
        sheet_name='TimeSeries_1971-2019',
        skiprows=1
    )
    for year in range(1971, 2019):
        energy.loc[energy[year] == '..', year] = 0

    energy = energy[(energy['Country'] == 'Australia') & (energy['NoFlow'] == '01. Production (ktoe)')]

    energy = energy[list(range(1971, 2019))].sum().reset_index()

    exit()
    start_index = -1
    min_year = get_min_data()
    max_year = get_max_year()
    dfs = [get_data_from_year(step) for step in range(min_year, max_year + 1, 1)]
    years = range(min_year, max_year + 1, 1)
    data = [go.Scatter(
        visible=False,
        mode='markers',
        text=df['Country Name'],
        x=df[str(years[index])],
        y=df['co2_per_capta'])
        for index, df in enumerate(dfs)]
    data[start_index]['visible'] = True

    steps = []
    for i in range(len(data)):
        step = dict(
            method='update',
            label=str(years[i]),
            args=[
                # Make the ith trace visible
                {'visible': [t == i for t in range(len(data))]},
                {'title.text': 'Year %d' % years[i]}],
        )
        steps.append(step)

    # Build sliders
    sliders = [go.layout.Slider(
        active=len(years) - 1,
        currentvalue={"prefix": "Year: "},
        pad={"t": 50},
        steps=steps
    )]

    layout = go.Layout(
        sliders=sliders,
        title={'text': 'Year %d' % years[start_index]}
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type="log", range=[log10(20), log10(200000)])
    fig.update_yaxes(type='log', range=[log10(0.01), log10(100)])
    fig.write_html('tmp3.html', auto_open=True)


def get_max_year():
    co = pd.read_csv("annual-co-emissions-by-region.csv").dropna()
    max_year_by_country = co.groupby(['Code'], sort=False)['Year'].max().reset_index()
    if max_year_by_country.max()['Year'] > 2019:
        max_year = 2019
    else:
        max_year = max_year_by_country.max()['Year']
    return max_year


def get_min_data():
    co = pd.read_csv("annual-co-emissions-by-region.csv").dropna()
    min_year_by_country = co.groupby(['Code'], sort=False)['Year'].min().reset_index()
    if min_year_by_country.min()['Year'] < 1960:
        min_year = 1960
    else:
        min_year = min_year_by_country.min()['Year']
    return min_year


if __name__ == '__main__':
    main()
