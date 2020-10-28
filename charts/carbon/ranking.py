from charts.carbon.carbon import carbon_data
from charts.geolocation.geolocation import join_on_iso_3

import numpy
3
def main():
    co = carbon_data().dropna()
    co = join_on_iso_3(co, 'Code')
    min_year, max_year = 1850, co['Year'].max()
    for year in range(min_year, max_year):
        data = co[co['Year'] == year].dropna(subset=['Continent'])
        data = data[data['Annual CO2 emissions (tonnes)'] > 0]
        data['rank'] = data['Annual CO2 emissions (tonnes)'].rank()


if __name__ == '__main__':
    main()
