import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';') 

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='sexe-slider',
        min=df['sexe'].min(),
        max=df['sexe'].max(),
        value=df['sexe'].min(),
        marks={str(sexe): str(sexe) for sexe in df['sexe'].unique()},
        step=None
    )
])


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







