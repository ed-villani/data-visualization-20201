from copy import deepcopy

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.power_plants.power_plant_colors import get_power_plant_color
from charts.power_plants.power_plants import read_power_plants, get_power_plants_types


def pp_per_year_cumsum():
    data = read_power_plants()
    power_plant_types = get_power_plants_types(data)
    # data = join_on_iso_3(data, 'country', two_americas=False)
    data = data.fillna(0).astype({"commissioning_year": 'int32'}).groupby(
        ['commissioning_year', 'primary_fuel']).count().reset_index()
    data = data[data['commissioning_year'] > 0]

    data[data["primary_fuel"] == power_plant_types[0]].cumsum()
    power_plant_types = list(power_plant_types)
    power_plant_types.pop(3)
    fig = make_subplots(rows=5, cols=3, subplot_titles=power_plant_types)

    for i in range(5):
        for j in range(3):
            if i * 3 + j == 14:
                break
            aux_data = deepcopy(data)
            aux_data = aux_data[aux_data["primary_fuel"] == power_plant_types[i * 3 + j]]
            fig.add_trace(go.Scatter(
                x=aux_data['commissioning_year'],
                y=aux_data['country'].cumsum(),
                name=power_plant_types[i * 3 + j],
                marker=dict(
                    color=get_power_plant_color(power_plant_types[i * 3 + j])
                ),
                mode='lines'
            ),
                row=i + 1, col=j + 1)

            fig.update_xaxes(range=[1896, 2018], row=i + 1, col=j + 1)

    fig.update_layout(title_text="Cumulative Power Plants per type in the period 1896-2018")

    # fig.write_html('tmp3.html', auto_open=True)
    # fig.show()
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


if __name__ == '__main__':
    pp_per_year_cumsum()
