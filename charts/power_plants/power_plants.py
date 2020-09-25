from copy import deepcopy
import pandas as pd
import numpy as np

from charts.geolocation.geolocation import join_on_iso_3

GLOBAL_POWER_PLANT_DB = '/Users/eduardovillani/git/data-visualization-20201/data/power_plants/global_power_plant_database.csv'


def read_power_plants():
    return pd.read_csv(GLOBAL_POWER_PLANT_DB)


def power_plants_pareto_generated():
    data = read_power_plants().dropna(subset=['estimated_generation_gwh']).groupby('primary_fuel').sum()['estimated_generation_gwh'].reset_index()
    data = data.sort_values('estimated_generation_gwh', ascending=False).reset_index(drop=True)
    proportion = data['estimated_generation_gwh'].tolist()
    proportion = np.cumsum(np.array(proportion) / sum(proportion))

    data['proportion'] = pd.Series(proportion)
    return data


def power_plants_pareto_capacity():
    data = read_power_plants().groupby('primary_fuel').sum()['capacity_mw'].reset_index()
    data = data.sort_values('capacity_mw', ascending=False).reset_index(drop=True)
    proportion = data['capacity_mw'].tolist()
    proportion = np.cumsum(np.array(proportion) / sum(proportion))

    data['proportion'] = pd.Series(proportion)
    return data


def power_plants_pareto_count():
    data = read_power_plants().groupby('primary_fuel').count()['latitude'].reset_index()
    data = data.sort_values('latitude', ascending=False).reset_index(drop=True)
    proportion = data['latitude'].tolist()
    proportion = np.cumsum(np.array(proportion) / sum(proportion))

    data['proportion'] = pd.Series(proportion)
    return data


def get_power_plants_types(data, country='World'):
    """
    Returns the power plants type for the data file sorted by the world median of capacity
    :param country:
    :param data:
    :return: power_pant_types
    """
    aux_data = deepcopy(data)
    if country == 'World':
        power_plant_types = aux_data
    else:
        power_plant_types = aux_data[country == aux_data['country_long']]
    del aux_data
    return power_plant_types.groupby(['primary_fuel'])['capacity_mw'].median().sort_values().axes[0]


def get_data_by_primary_fuel(data, power_plant_type):
    return deepcopy(data[power_plant_type == data['primary_fuel']])


def set_visible_by_option(entity, entity_order_list):
    return [True if e == entity else False for e in entity_order_list]


def total_capacity_per_country():
    data = read_power_plants()
    data = join_on_iso_3(data, 'country', two_americas=False)
    capacity_per_country = data.groupby(['country']).sum()['capacity_mw']
    number_per_country = data.groupby(['country']).count()['country_long'].reset_index()
    country_names = capacity_per_country.axes[0].to_frame().reset_index(drop=True)
    capacity_per_country = capacity_per_country.reset_index(drop=True)
    country_names['quantity'] = number_per_country['country_long']
    country_names['capacity_mw'] = capacity_per_country
    country_names = join_on_iso_3(country_names, 'country', two_americas=False)
    return country_names
