import pandas as pd
import plotly.graph_objects as go


def main():
    co = pd.read_csv("annual-co-emissions-by-region.csv").dropna()
    max_year_by_country = co.groupby(['Code'], sort=False)['Year'].max().reset_index()
    co = co[co['Year'] == max_year_by_country['Year'].max()]
    gdp = pd.read_excel("gdp_per_year.xls")[['Country Name',
                                             'Country Code',
                                             str(max_year_by_country['Year'].max())]].dropna()
    pop = pd.read_excel("pop_per_year_per_country.xls")[['Country Name',
                                             'Country Code',
                                             str(max_year_by_country['Year'].max())]].dropna()
    pop = pop.rename(columns={"2018": "2018_pop", "Country Code": "code_pop"})[['2018_pop', 'code_pop']]

    data = co.join(gdp.set_index('Country Code'), on='Code')
    data = data.join(pop.set_index("code_pop"), on='Code').dropna(subset=['2018', 'Country Name', '2018_pop'])
    data['co2_per_capta'] = data['Annual CO2 emissions (tonnes)']/data['2018_pop']
    fig = go.Figure()
    fig.add_trace(go.Scatter(text=data['Country Name'], x=data[str(max_year_by_country['Year'].max())],
                             y=data['co2_per_capta'],
                             mode='markers'))
    fig.update_xaxes(type="log")
    fig.update_yaxes(type='log')
    fig.write_html('tmp3.html', auto_open=True)


if __name__ == '__main__':
    main()
