import pandas as pd
import plotly.graph_objects as go


def main():
    co = pd.read_csv("annual-co-emissions-by-region.csv")
    continent_list = [
        'Europe',
        'Asia',
        'North America',
        'South America',
        'Africa',
        'Oceania'
    ]
    # co_per_continent = co[co['Entity'].isin(continent_list)][['Entity', 'Year', 'Annual CO2 emissions (tonnes)']]

    fig = go.Figure()
    for c in continent_list:
        data = co[(co['Entity'] == c) & (co['Annual CO2 emissions (tonnes)'] > 0)]
        fig.add_trace(go.Scatter(x=data['Year'], y=data['Annual CO2 emissions (tonnes)'],
                                 name=c,
                                 mode='lines'))
    fig.write_html('tmp3.html', auto_open=True)


if __name__ == '__main__':
    main()
