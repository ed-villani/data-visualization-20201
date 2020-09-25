import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.power_plants.power_plant_colors import join_colors
from charts.power_plants.power_plants import power_plants_pareto_capacity


def capacity_pareto():
    data = power_plants_pareto_capacity()
    data = join_colors(data, 'primary_fuel')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=data['primary_fuel'],
        y=data['capacity_mw'],
        marker=dict(
            color=data['Color']
        ),
        name='Quantity'

    ),
        secondary_y=False)

    fig.add_trace(go.Scatter(
        x=data['primary_fuel'],
        y=data['proportion'] * 100,
        name='Pareto Proportion'
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=data['primary_fuel'],
        y=[80 for _ in data['primary_fuel']],
        name='80% Pareto Proportion',
        marker=dict(
            color='black'
        ),
    ), secondary_y=True)

    fig.update_layout(
        yaxis_type="log",
        title={
            'text': "Power Plant Capacity and its Proportion",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Capacity (MW)",
        xaxis_title="Power Plant Type",
        yaxis2=dict(
            title="Proportion (%)"
        )
    )
    fig['layout']['yaxis2'].update(range=[0, 105], autorange=False)
    # fig.write_html('tmp3.html', auto_open=True)
    return plotly.offline.plot(figure_or_data=fig, include_plotlyjs=False, output_type='div')


if __name__ == '__main__':
    capacity_pareto()
