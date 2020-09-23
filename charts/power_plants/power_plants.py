from copy import deepcopy
import pandas as pd

GLOBAL_POWER_PLANT_DB = '/Users/eduardovillani/git/data-visualization-20201/data/power_plants/global_power_plant_database.csv'


def read_power_plants():
    return pd.read_csv(GLOBAL_POWER_PLANT_DB)


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
