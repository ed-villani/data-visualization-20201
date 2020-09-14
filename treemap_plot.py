import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def main():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/sales_success.csv')
    print(df.head())

    levels = ['salesperson', 'county', 'region']  # levels used for the hierarchical chart
    color_columns = ['sales', 'calls']
    value_column = 'calls'

    def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
        """
        Build a hierarchy of levels for Sunburst or Treemap charts.

        Levels are given starting from the bottom to the top of the hierarchy,
        ie the last level corresponds to the root.
        """
        df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
            dfg = df.groupby(levels[i:]).sum()
            dfg = dfg.reset_index()
            df_tree['id'] = dfg[level].copy()
            if i < len(levels) - 1:
                df_tree['parent'] = dfg[levels[i + 1]].copy()
            else:
                df_tree['parent'] = 'total'
            df_tree['value'] = dfg[value_column]
            df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
            df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        total = pd.Series(dict(id='total', parent='',
                               value=df[value_column].sum(),
                               color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
        df_all_trees = df_all_trees.append(total, ignore_index=True)
        return df_all_trees

    df_all_trees_1 = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    data = pd.read_csv("global_power_plant_database.csv")
    regions = pd.read_excel("contry_continent.xlsx")
    data = data.join(regions.set_index('ISO (3)'), on='country')
    capacity_per_country = data.groupby(['country']).sum()['capacity_mw']
    number_per_country = data.groupby(['country']).count()['country_long'].reset_index()
    country_names = capacity_per_country.axes[0].to_frame().reset_index(drop=True)
    capacity_per_country = capacity_per_country.reset_index(drop=True)

    country_names['quantity'] = number_per_country['country_long']
    country_names['capacity_mw'] = capacity_per_country
    country_names = country_names.join(regions.set_index('ISO (3)'), on='country')
    levels = ['Country', 'Region', 'Continent']  # levels used for the hierarchical chart
    color_columns = ['quantity', 'capacity_mw']
    value_column = 'capacity_mw'
    df = country_names
    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    average_score = df['quantity'].sum() / df['capacity_mw'].sum()
    # average_score = np.average(df['capacity_mw']/(10**6), weights=df['quantity'])
    # average_score = df['sales'].sum() / df['calls'].sum()

    fig = make_subplots(1, 2, specs=[[{"type": "domain"}, {"type": "domain"}]], )

    fig = go.Figure()
    fig.add_trace(go.Treemap(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='RdBu'),
        hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
        name=''
    ))
    #
    # fig.add_trace(go.Treemap(
    #     labels=df_all_trees['id'],
    #     parents=df_all_trees['parent'],
    #     values=df_all_trees['value'],
    #     branchvalues='total',
    #     marker=dict(
    #         colors=df_all_trees['color'],
    #         colorscale='RdBu',
    #         cmid=average_score),
    #     hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
    #     maxdepth=2
    # ), 1, 2)

    # fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))
    fig.write_html('tmp3.html', auto_open=True)


if __name__ == '__main__':
    main()
