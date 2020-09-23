from charts.power_plants.boxplot import chart_boxplot
from charts.power_plants.map_scatter_plot import map_scatter_plot


class PowerPlantsTemplate:
    def __new__(cls, boxplot, map_scatter_plot):
        template = f"""<html>
    <head>
        <link rel="stylesheet" href="style.css" type="text/css">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="map">{map_scatter_plot}</div>
         <div class="container">
            <div class="left">{boxplot[0]}</div>
            <div class="right"{boxplot[1]}</div>
        </div
    </body>

    </html>"""

        with open('/Users/eduardovillani/git/data-visualization-20201/teste.html', 'w') as f:
            f.write(template)


def main():
    map_scatter = map_scatter_plot()
    PowerPlantsTemplate([chart_boxplot() for _ in range(2)], map_scatter)


if __name__ == '__main__':
    main()
