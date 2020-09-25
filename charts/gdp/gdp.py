import pandas as pd

GDP_DATA_PATH = '/Users/eduardovillani/git/data-visualization-20201/data/gdp/gdp_per_year.xls'


def gdp_data():
    return pd.read_excel(GDP_DATA_PATH)


def get_gdp_by_year(year, drop_na=True):
    if drop_na:
        return gdp_data()[
            ['Country Name',
             'Country Code',
             str(year)]
        ].dropna()

    return gdp_data()[
        ['Country Name',
         'Country Code',
         str(year)]
    ]


def join_gdp_by_iso3(other, on, year=False):
    if year:
        return other.join(get_gdp_by_year(year).set_index('Country Code'), on=on)
    return other.join(gdp_data().set_index('Country Code'), on=on)
