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
        <link rel="stylesheet" href="style/style.css" type="text/css">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>

    <body>
        <h1 class="title">Power Plants, electricity, Environment and Society</h1>
        <h2 class="subtitle">How electricity generation interacts with society?</h2>
        <div>
            <p>
                This is a project for 2020/1 Data Visualization class. The aim of this project is
                to discover how power plants and its generation capacity interacts with society
                and the impacts in different levels of human life. 
            </p>
            <p>
                We start with the definition of the power plants type presents in the project. 
            </p>
            <ul>
                <li>Storage: Renewable. A type of hydro-power plant. It can store gravitational potential energy by 
pumping water from lower to a higher elevation.</li> 
                <li>Solar: Renewable. Uses sun radiation to generate electricity. </li>
                <li>Waste: Not exactly Renewable, but Sustainable. It's  a kind of carbon-negative thermal power plant. 
Uses wast to generate electricity.</li>
                <li>Wave and Tidal: Renewable. Uses tides/gravity to generate electricity.</li>
                <li>Oil: Non-Renewable. Uses oils to generate electricity.</li>
                <li>Biomass: Renewable. Uses biomass to generate electricity. Biomass is plant or animal material. </li>
                <li>Hydro: Renewable. Uses water to generate electricity.</li>
                <li>Wind: Renewable. Uses wind to generate electricity.</li>
                <li>Cogeneration: Not exactly Renewable, but Sustainable. Uses some fuel (oil or solar for ex.) to 
generate electricity.</li> 
                <li>Petcoke: Non-Renewable. It's a kind of Oil Power Plant. Uses petcoke to generate electricity.</li>
                <li>Gas: Non-Renewable. Uses natural gas to generate electricity.</li>
                <li>Coal: Non-Renewable. Uses coal to generate electricity.</li>
                <li>Nuclear: Not exactly Renewable, but Sustainable. It uses nuclear reactions to generate 
electricity.</li> 
                <li>Other: Any other kind of power plant. </li>
            </ul>
        </div>
        
        <div>{map_scatter_plot}</div>
        <div>{boxplot[0]}</div>
        <div>{treemap}</div>
        <div>{pareto[0]}</div>
        <div>{pareto[1]}</div>

        <div>
            <p>
                The history of human development is also the history of CO2. Since the begging of the Industrial 
Revolution,  CO2 level in Earth's atmosphere is rising. We can notice some behaviour on CO2 over great history events.
We can also notice how the developed countries are slowly emitting less CO2 over the last two decades, probably because
in a change of a non-renewable energy mix to a renewable one.
            </p>
            <div id="row-parent">
                <div id="row">
                    <div>
                        <div class="box red"><p class="co2">World War I</p></div> 
                    </div>
                    <div>
                        <div class="box red"><p class="co2">29' Crash</p></div> 
                    </div>
                    <div>
                        <div class="box red"><p class="co2">World War II</p></div> 
                    </div>
                    <div>
                        <div class="box red"><p class="co2">Asia's Tigers</p></div> 
                    </div>
                    <div>
                        <div class="box red"><p class="co2">USSR ends</p></div> 
                    </div>
                    <div>
                        <div class="box red"><p class="co2">2008 Crash</p></div> 
                    </div>
                </div>
            </div>

        <div>{timeline}</div>
        <div>{gdp_v_carbon}</div>
    </body>

    </html>"""

        with open('/Users/eduardovillani/git/data-visualization-20201/templates/index.html', 'w') as f:
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
