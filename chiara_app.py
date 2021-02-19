import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# dataframe for first figure FRANCE
df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';') 
df1=df.groupby(['jour','sexe'])['hosp'].sum().unstack()
df1.reset_index(inplace=True)
df1=df1.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})

# dataframe for second figure ISERE
df['dep'].astype(str)
dfnew=df.loc[df['dep'] == '38']
df2=dfnew.groupby(['jour','sexe'])['hosp'].sum().unstack()
df2.reset_index(inplace=True)
df2=df2.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})

# dataframe for third figure SAVOIE
dfnew=df.loc[df['dep'] == '73']
df3=dfnew.groupby(['jour','sexe'])['hosp'].sum().unstack()
df3.reset_index(inplace=True)
df3=df3.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})

# dataframe for forth figure SAVOIE
dfnew=df.loc[df['dep'] == '26']
df4=dfnew.groupby(['jour','sexe'])['hosp'].sum().unstack()
df4.reset_index(inplace=True)
df4=df4.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})

# dataframe for forth figure SAVOIE
dfnew=df.loc[df['dep'] == '69']
df5=dfnew.groupby(['jour','sexe'])['hosp'].sum().unstack()
df5.reset_index(inplace=True)
df5=df5.rename(columns={0:'Total', 1:'Hommes', 2:'Femmes'})


fig1 = px.line(df1, x='jour', y=['Total','Hommes','Femmes'])
fig2 = px.line(df2, x='jour', y=['Total','Hommes','Femmes'])
fig3 = px.line(df3, x='jour', y=['Total','Hommes','Femmes'])
fig4 = px.line(df4, x='jour', y=['Total','Hommes','Femmes'])
fig5 = px.line(df5, x='jour', y=['Total','Hommes','Femmes'])

@app.callback(
    Output('example-graph1', 'figure'),
    Input('mydrop', 'value'))
def myfigure(location):
    if location == 'France':
        df=df1
    elif location == 'Isere' :
        df=df2
    elif location == 'Savoie' :
        df=df3
    elif location == 'Drome' :
        df=df4
    else :
        df=df5
    fig = px.line(df, x='jour', y=['Total','Hommes','Femmes'])
    return fig


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

    dcc.Dropdown(
        id='mydrop',
        options=[
            {'label': 'France', 'value': 'France'},
            {'label': 'Isere', 'value': 'Isere'},
            {'label': 'Savoie', 'value': 'Savoie'},
            {'label': 'Drome', 'value': 'Drome'},
            {'label': 'Rhone', 'value': 'Rhone'},
        ],     
        value='France'
    ),

    dcc.Graph(
        id='example-graph1',
    ),

   
])

if __name__ == '__main__':
    app.run_server(debug=True)