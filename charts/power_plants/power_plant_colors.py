import pandas as pd

POWER_PLANT_COLORS = '/Users/eduardovillani/git/data-visualization-20201/data/power_plants/power_plant_colors.csv'


def get_power_plant_color(power_plant):
    data = pd.read_csv(POWER_PLANT_COLORS)
    color = data[data['Type'] == power_plant]['Color'].values[0]
    return color
