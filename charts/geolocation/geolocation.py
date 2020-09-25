from copy import deepcopy

import pandas as pd

GEO_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/geolocations/country_continent.xlsx'
COLOR_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/geolocations/continents_colors.csv'


def geo_locations_data(two_americas=True):
    country_continent = pd.read_excel(GEO_DATA_PATH)
    continent_color_data = pd.read_csv(COLOR_DATA_PATH)

    if two_americas:
        country_continent.loc[country_continent['Region'] == 'North America', 'Continent'] = 'North America'
        country_continent.loc[country_continent['Region'] == 'Central America', 'Continent'] = 'North America'
        country_continent.loc[country_continent['Region'] == 'West Indies', 'Continent'] = 'North America'
        country_continent.loc[country_continent['Region'] == 'South America', 'Continent'] = 'South America'

    country_continent = country_continent.join(continent_color_data.set_index('Continent_Color'), on='Continent')

    return country_continent


def join_on_iso_3(other, on, **kwargs):
    data = deepcopy(other)
    return data.join(geo_locations_data(**kwargs).set_index('ISO (3)'), on=on)


def get_continents():
    return pd.read_csv(COLOR_DATA_PATH)['Continent_Color'].to_list()


def continent_color(continent):
    data = pd.read_csv(COLOR_DATA_PATH)
    return data[data['Continent_Color'] == continent]['Color'].values[0]
