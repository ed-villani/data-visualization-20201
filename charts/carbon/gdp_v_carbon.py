from math import log10

import plotly
import plotly.graph_objects as go

from charts.carbon.carbon import data_by_year, carbon_data
from charts.gdp.gdp import join_gdp_by_iso3
from charts.geolocation.geolocation import join_on_iso_3
from charts.population.population import get_pop_by_year


def get_data_from_year(current_year):
    co = data_by_year(current_year)
    pop = get_pop_by_year(current_year)

    data = join_gdp_by_iso3(co, 'Code', current_year)
    data = join_on_iso_3(data, 'Code')
    data = data.join(pop.set_index("code_pop"), on='Code').dropna(
        subset=[str(current_year), 'Country Name', f'{str(current_year)}_pop'])
    data['co2_per_capta'] = data['Annual CO2 emissions (tonnes)'] / data[f'{str(current_year)}_pop']
    data['co2_per_capta_str'] = data['co2_per_capta'].map('{:,.2f} Tonnes / per capta'.format)
    data[f'{str(current_year)}_pop_str'] = data[f'{str(current_year)}_pop'].map('{:,.0f}'.format)
    data[f"{str(current_year)}_str"] = data[str(current_year)].map('${:,.2f}'.format)
    return data


def scatter_plot():
    start_index = -1
    min_year = get_min_data()
    max_year = get_max_year()
    dfs = [get_data_from_year(step) for step in range(min_year, max_year + 1, 1)]
    years = range(min_year, max_year + 1, 1)
    data = [
        go.Scatter(
            visible=False,
            mode='markers',
            text="Country: " + df['Country Name'] + '<br>CO2 per Capita: ' + df['co2_per_capta_str'].astype(
                str) + '<br>Population: ' + df[f'{str(years[index])}_pop_str'].astype(str) + "<br>GDPPC: " + df[f'{str(years[index])}_str'],
            x=df[str(years[index])],
            y=df['co2_per_capta'],
            marker=dict(
                color=df['Color']
            ),
            name=''
        ) for index, df in enumerate(dfs)
    ]

    data[start_index]['visible'] = True

    steps = [
        dict(
            method='update',
            label=str(years[i]),
            args=[
                {'visible': [t == i for t in range(len(data))]},
                {'title.text': 'GDPPC V. CO2 per Capita for Year %d' % years[i]}],
        ) for i in range(len(data))
    ]

    # Build sliders
    sliders = [
        go.layout.Slider(
            active=len(years) - 1,
            currentvalue={"prefix": "Year "},
            pad={"t": 50},
            steps=steps
        )
    ]

    layout = go.Layout(
        sliders=sliders
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type="log", range=[log10(20), log10(200000)])
    fig.update_yaxes(type='log', range=[log10(0.01), log10(100)])
    fig.update_layout(
        title={
            'text': 'GDPPC V. CO2 per Capita for Year %d' % years[start_index],
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="CO2 (Tonnes per capita)",
        xaxis_title="GDPPC (U$)"
    )
    # fig.write_html('tmp3.html', auto_open=True)
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


def get_max_year():
    co = carbon_data().dropna()
    max_year_by_country = co.groupby(['Code'], sort=False)['Year'].max().reset_index()
    if max_year_by_country.max()['Year'] > 2019:
        max_year = 2019
    else:
        max_year = max_year_by_country.max()['Year']
    return max_year


def get_min_data():
    co = carbon_data().dropna()
    min_year_by_country = co.groupby(['Code'], sort=False)['Year'].min().reset_index()
    if min_year_by_country.min()['Year'] < 1960:
        min_year = 1960
    else:
        min_year = min_year_by_country.min()['Year']
    return min_year


if __name__ == '__main__':
    scatter_plot()
