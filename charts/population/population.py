import pandas as pd

POPULATION_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/population/pop_per_year_per_country.xls'


def population_data():
    return pd.read_excel(POPULATION_DATA_PATH)


def get_pop_by_year(year, drop_na=True):
    if drop_na:
        data = population_data().dropna()
    else:
        data = population_data()
    data = data[['Country Name',
                 'Country Code',
                 str(year)]]
    data = data.rename(columns={str(year): f"{str(year)}_pop", "Country Code": "code_pop"})
    return data[[f'{str(year)}_pop', 'code_pop']]
