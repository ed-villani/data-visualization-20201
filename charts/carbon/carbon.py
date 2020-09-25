import pandas as pd

CARBON_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/carbon/annual-co-emissions-by-region.csv'


def carbon_data():
    return pd.read_csv(CARBON_DATA_PATH)


def data_by_year(year, drop_na=True):
    if drop_na:
        data = carbon_data().dropna()
    else:
        data = carbon_data()
    data = data[data['Year'] == year]
    return data
