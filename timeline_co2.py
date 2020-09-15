import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    co = pd.read_csv("annual-co-emissions-by-region.csv")
    co = co.dropna()
    # co = co[co['Year'] >= 1971]
    country_continent = pd.read_excel("contry_continent.xlsx")
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

    energy = pd.read_excel(
        'World_Energy_Balances_Highlights_(2020_edition).xlsx',
        sheet_name='TimeSeries_1971-2019',
        skiprows=1
    )

    fig = make_subplots(rows=2, cols=1)
    for c, color in zip(continent_list, colors):
        data = co[(co['Continent'] == c) & (co['Annual CO2 emissions (tonnes)'] > 0)]
        fig.add_trace(go.Scatter(x=data['Year'], y=data['Annual CO2 emissions (tonnes)'],
                                 name=c,
                                 mode='lines',
                                 legendgroup="group",
                                 line_color=color
                                 ), 1, 1)
        # fig.add_trace(go.Scatter(x=data['Year'], y=data['Annual CO2 emissions (tonnes)'],
        #                          mode='lines',
        #                          legendgroup="group",
        #                          stackgroup='one',
        #                          groupnorm='percent',
        #                          line_color=color,
        #                          showlegend=False), 2, 1)

    country_continent = pd.read_excel("contry_continent.xlsx")
    country_continent.loc[country_continent['Region'] == 'North America', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'Central America', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'West Indies', 'Continent'] = 'North America'
    country_continent.loc[country_continent['Region'] == 'South America', 'Continent'] = 'South America'
    energy.loc[energy['Country'] == 'Korea', 'Country'] = 'Korea, South'
    energy.loc[energy['Country'] == 'Slovak Republic', 'Country'] = "Slovakia"
    energy.loc[energy['Country'] == 'People\'s Republic of China', 'Country'] = 'China'
    energy = energy[energy['Flow'] == 'Production (ktoe)']
    data = energy.join(country_continent.set_index('Country'), on='Country')
    data = data[['Country', 'Continent'] + list(range(1971, 2019))].dropna()

    for year in range(1971, 2019):
        data.loc[energy[year] == '..', year] = 0
        data.loc[energy[year] == 'c', year] = 0
    data = data[data.columns[1:]].groupby('Continent').sum().T.reset_index()
    for c, color in zip(continent_list, colors):
        fig.add_trace(go.Scatter(x=data['index'], y=data[c],
                                 name=c,
                                 mode='lines',
                                 legendgroup="group",
                                 line_color=color
                                 ), 2, 1)
    fig.write_html('tmp3.html', auto_open=True)


if __name__ == '__main__':
    main()
