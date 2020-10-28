from charts.population.population import get_pop_by_year
from charts.power_plants.power_plants import read_power_plants


def main():
    data = read_power_plants()
    pop = get_pop_by_year(2017)
    data = data.groupby(['country', 'country_long']).sum().reset_index()[
        ['country', 'country_long', 'estimated_generation_gwh']]
    data = data.sort_values('estimated_generation_gwh')
    data = data[data['estimated_generation_gwh'] > 0]
    data = data.join(pop.set_index("code_pop"), on='country').dropna()


if __name__ == '__main__':
    main()
