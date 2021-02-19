import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import geopandas as gpd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';') 

"""
###data
df1=df.groupby(['jour','sexe'])['hosp'].sum().unstack()
df1.reset_index(inplace=True)
df1=df1.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})
fig = px.line(df1, x='jour', y=['Total','Hommes','Femmes'])


###
df2 = df.query("sexe==0")
df2=df2[['hosp','rea','rad','dc']].groupby(df2['jour']).sum()
df2.reset_index(inplace=True)
fig2 = px.area(df2, x="jour", y=['rea','dc', 'hosp'])
"""

### data preprocess pour carte

sf = gpd.read_file('departements-version-simplifiee.geojson')
dep_to_check = set(sf.code.unique())
df_carte = df.loc[df.dep.isin(dep_to_check) == True]
df_carte = df_carte.query("sexe==0")
df_carte = df_carte.loc[df_carte['jour']=='2021-02-18']



fig_carte = px.choropleth_mapbox(df_carte, geojson=sf, color="dc",
                           locations="dep", featureidkey="properties.code",
                           center={"lat": 46.22, "lon": 2.21},
                           mapbox_style="carto-positron", zoom=5)



app.layout = html.Div(children=[
    html.H1(children='Covid Dashboard'),

    html.Div([
        html.P('These graphs show some analysis on covid pandemic in France.'),
        html.P("from https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/ ")
    ], style={'marginBottom': 50, 'marginTop': 25}
    ),

    html.Div(children='''
        Group Data+8: Ahlem, Elena, Chiara.
    '''),

    dcc.Graph(
        id='carte',
        figure=fig_carte,
        style = {'display': 'inline-block'}
    ),

    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='sexe-slider',
        min=df['sexe'].min(),
        max=df['sexe'].max(),
        value=df['sexe'].min(),
        marks={str(sexe): f"{['Total', 'Hommes', 'Femmes'][sexe]}" for sexe in df['sexe'].unique()},
        step=None,
    )
    
],
style = {'display': 'inline-block', 'width': '48%'})

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('sexe-slider', 'value'))
def update_figure(selected_sexe):
    df2= df[df.sexe == selected_sexe]
    df2=df2[['hosp','rea','rad','dc']].groupby(df2['jour']).sum()
    df2.reset_index(inplace=True)

    fig = px.area(df2, x="jour", y=['rea','dc', 'hosp'])

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)