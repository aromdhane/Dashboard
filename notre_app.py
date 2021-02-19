import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';') 
df1=df.groupby(['jour','sexe'])['hosp'].sum().unstack()
df1.reset_index(inplace=True)
df1=df1.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})


fig = px.line(df1, x='jour', y=['Total','Hommes','Femmes'])

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='example-graph2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)