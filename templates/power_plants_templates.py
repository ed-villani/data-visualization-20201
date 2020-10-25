from charts.carbon.gdp_v_carbon import scatter_plot
from charts.carbon.timeline_co2 import timeline
from charts.power_plants.boxplot import chart_boxplot
from charts.power_plants.map_scatter_plot import map_scatter_plot
from charts.power_plants.pareto_power_plant_capacity_chart import capacity_pareto
from charts.power_plants.pareto_power_plant_chart import quantity_pareto
from charts.power_plants.treemap_capacity_plot import treemap_capacity


class PowerPlantsTemplate:
    def __new__(cls, boxplot, map_scatter_plot, treemap, pareto, timeline, gdp_v_carbon):
        template = f"""<html>
    <head>
        <link rel="stylesheet" href="style.css" type="text/css">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="map">{map_scatter_plot}</div>
         <div class="container">
            <div class="left">{boxplot[0]}</div>
        <div>{treemap}</div>
        <div>{pareto[0]}</div>
        <div>{pareto[1]}</div>
        <div>{timeline}</div>
        <div>{gdp_v_carbon}</div>
        </div
    </body>

    </html>"""

        with open('/index.html', 'w') as f:
            f.write(template)


def main():
    map_scatter = map_scatter_plot()
    treemap = treemap_capacity()
    PowerPlantsTemplate(
        [chart_boxplot() for _ in range(1)],
        map_scatter,
        treemap,
        [capacity_pareto(), quantity_pareto()],
        timeline(),
        scatter_plot()
    )


if __name__ == '__main__':
    main()
