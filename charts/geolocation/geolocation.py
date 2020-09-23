from copy import deepcopy

import pandas as pd

GEO_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/geolocations/country_continent.xlsx'


def geo_locations_data():
    return pd.read_excel(GEO_DATA_PATH)


def join_on_iso_3(other, on):
    data = deepcopy(other)
    return data.join(geo_locations_data().set_index('ISO (3)'), on=on)
