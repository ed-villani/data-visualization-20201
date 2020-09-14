from math import log10

import pandas as pd
import plotly.graph_objects as go


def get_data_from_year(current_year):
    co = pd.read_csv("annual-co-emissions-by-region.csv").dropna()
    co = co[co['Year'] == current_year]
    gdp = pd.read_excel("gdp_per_year.xls")[['Country Name',
                                             'Country Code',
                                             str(current_year)]].dropna()
    pop = pd.read_excel("pop_per_year_per_country.xls")[['Country Name',
                                                         'Country Code',
                                                         str(current_year)]].dropna()
    pop = pop.rename(columns={str(current_year): f"{str(current_year)}_pop", "Country Code": "code_pop"})[
        [f'{str(current_year)}_pop', 'code_pop']]

    data = co.join(gdp.set_index('Country Code'), on='Code')
    data = data.join(pop.set_index("code_pop"), on='Code').dropna(
        subset=[str(current_year), 'Country Name', f'{str(current_year)}_pop'])
    data['co2_per_capta'] = data['Annual CO2 emissions (tonnes)'] / data[f'{str(current_year)}_pop']
    return data


def main():
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
        active=len(years)-1,
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
