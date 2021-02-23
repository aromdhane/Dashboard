import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';') 

#data pour vaccination
#import des données
df_vacc=pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530", delimiter=',')
df_tot_vacc=df_vacc.loc[df_vacc['vaccin']==0]

#pour la construction du dropdown
col_options=[]
num_reg=[ 1,  2,  3,  4,  6,  7, 11, 24, 27, 28, 32, 44, 52, 53, 75, 76, 84,
       93, 94]
list_reg =['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte',
       'Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté',
       'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire',
       'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie',
       'Auvergne-Rhône-Alpes', "Provence-Alpes-Côte d'Azur", 'Corse']
dictionary = dict(zip(num_reg, list_reg))

for key, values in dictionary.items():
    my_dict={'label':values, 'value':key}
    col_options.append(my_dict)

### data preprocess pour carte

sf = gpd.read_file('departements-version-simplifiee.geojson')
dep_to_check = set(sf.code.unique())
df_carte = df.loc[df.dep.isin(dep_to_check) == True]
df_carte = df_carte.query("sexe==0")
df_carte = df_carte.loc[df_carte['jour']=='2021-02-18']



fig_carte = px.choropleth_mapbox(df_carte, geojson=sf, color="dc",
                           locations="dep", featureidkey="properties.code",
                           center={"lat": 46.22, "lon": 2.21},
                           mapbox_style="carto-positron", zoom=4,
                           )



app.layout =  html.Div(children=[
    html.H1(children='Covid Dashboard', style={'textAlign': 'center','color' : colors['text']}),
    html.Div([
        html.P('These graphs show some analysis on covid pandemic in France.'),
        html.P("from https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/ ")
    ], 
    style={'marginBottom': 50, 'marginTop': 25, 'textAlign': 'center'}
    ),
    
    html.Div(html.H2('Situation hospitalière Globale'),  
             ),
    
    dcc.Slider(
        id='sexe-slider',
        min=df['sexe'].min(),
        max=df['sexe'].max(),
        value=df['sexe'].min(),
        marks={str(sexe): f"{['Total','Hommes','Femmes'][sexe]}" for sexe in df['sexe'].unique()},
        step=None,
        tooltip={'placement':'topLeft'},   
    ),
    dcc.Graph(id='graph-with-slider'),
    

    #suivi de la vaccination par région
    html.Div(html.H1("Suivi vaccination par région")
    ),
    dcc.Dropdown(id='reg', value=1, options=col_options),
    dcc.Graph(id='graph_vacc', figure={}),

    
    #new graph with dropdown hospitalisation et rea pour chaque departement
    html.Div(html.H2('Situation hospitalière départementale')),
    dcc.Dropdown(
        id='mydrop',
        options=[
            {'label' : 'Ain', 'value' :'01'},
            {'label' : 'Aisne', 'value' :'02'},
            {'label' : 'Allier', 'value' :'03'},
            {'label' : 'Alpes-de-Haute-Provence ', 'value' :'04'},
            {'label' : 'Hautes-alpes ', 'value' :'05'},
            {'label' : 'Alpes-maritimes', 'value' :'06'},
            {'label' : ' Ardèche', 'value' :'07'},
            {'label' : 'Ardennes ', 'value' :'08'},
            {'label' : ' Ariège', 'value' :'09'},
            {'label' : 'Aube', 'value' :'10'},
            {'label' : 'aude', 'value' :'11'},
            {'label' : 'Aveyron', 'value' :'12'},
            {'label' : 'Bouches-du-Rhône', 'value' :'13'},
            {'label' : 'Calvados', 'value' :'14'},
            {'label' : 'Calvados', 'value' :'14'},
            {'label' : 'Cantal', 'value' :'15'},
            {'label' : 'Charente', 'value' :'16'},
            {'label' : 'Charente-maritime', 'value' :'17'},
            {'label' : 'Cher', 'value' :'18'},
            {'label' : 'Corrèze', 'value' :'19'},
            {'label' : 'Corse-du-sud ', 'value' :'2A'},
            {'label' : 'Haute-Corse', 'value' :'2B'},
            {'label' : "Côte-d'Or", 'value' :'21'},
            {'label' : "Côte-d'Armor", 'value' :'22'},
            {'label' : "Creuse", 'value' :'23'},
            {'label' : "Dordogne", 'value' :'24'},
            {'label' : "Doubs", 'value' :'25'},
            {'label' : "Drôme", 'value' :'26'},
            {'label' : "Eure", 'value' :'27'},
            {'label' : "Eure et loir", 'value' :'28'},
            {'label' : "Finistère", 'value' :'29'},
            {'label' : "Gard", 'value' :'30'},
            {'label' : "Haute garonne", 'value' :'31'},
            {'label' : "Gers", 'value' :'32'},
            {'label' : "Gironde", 'value' :'33'},
            {'value':'34', 'label': 'Hérault'}, 
            {'value':'35', 'label': 'Ille-et-Vilaine'}, 
            {'value':'36', 'label': 'Indre'}, 
            {'value':'37', 'label': 'Indre-et-Loire'},
            {'value':'38', 'label': 'Isère'},  
            {'value':'39','label': 'Jura'}, 
            {'value':'40','label': 'Landes'}, 
            {'value':'41','label': 'Loir-et-Cher'}, 
            {'value':'42','label': 'Loire'}, 
            {'value':'43','label': 'Haute-Loire'},
            {'value':'44','label': 'Loire-Atlantique'}, 
            {'value':'45','label': 'Loiret'}, 
            {'value':'46','label': 'Lot'}, 
            {'value':'47','label': 'Lot-et-Garonne'}, 
            {'value':'48','label': 'Lozère'},
            {'value':'49','label': 'Maine-et-Loire'}, 
            {'value':'50','label': 'Manche'}, 
            {'value':'51','label': 'Marne'}, 
            {'value':'52','label': 'Haute-Marne'}, 
            {'value':'53','label': 'Mayenne'},
            {'value':'54','label': 'Meurthe-et-Moselle'}, 
            {'value':'55','label': 'Meuse'}, 
            {'value':'56','label': 'Morbihan'}, 
            {'value':'57','label': 'Moselle'}, 
            {'value':'58','label': 'Nièvre'}, 
            {'value':'59','label': 'Nord'},
            {'value':'60','label': 'Oise'}, 
            {'value':'61','label': 'Orne'}, 
            {'value':'62','label': 'Pas-de-Calais'}, 
            {'value':'63','label': 'Puy-de-Dôme'}, 
            {'value':'64','label': 'Pyrénées-Atlantiques'},
            {'value':'65','label': 'Hautes-Pyrénées'}, 
            {'value':'66','label': 'Pyrénées-Orientales'}, 
            {'value':'67','label': 'Bas-Rhin'}, 
            {'value':'68','label': 'Haut-Rhin'}, 
            {'value':'69','label': 'Rhône'},
            {'value':'70','label': 'Haute-Saône'}, 
            {'value':'71','label': 'Saône-et-Loire'}, 
            {'value':'72','label': 'Sarthe'}, 
            {'value':'73','label': 'Savoie'}, 
            {'value':'74','label': 'Haute-Savoie'},
            {'value':'75','label': 'Paris'}, 
            {'value':'76','label': 'Seine-Maritime'}, 
            {'value':'77','label': 'Seine-et-Marne'}, 
            {'value':'78','label': 'Yvelines'}, 
            {'value':'79','label': 'Deux-Sèvres'},
            {'value':'80','label': 'Somme'}, 
            {'value':'81','label': 'Tarn'}, 
            {'value':'82','label': 'Tarn-et-Garonne'}, 
            {'value':'83','label': 'Var'}, 
            {'value':'84','label': 'Vaucluse'}, 
            {'value':'85','label': 'Vendée'},
            {'value':'86','label': 'Vienne'}, 
            {'value':'87','label': 'Haute-Vienne'}, 
            {'value':'88','label': 'Vosges'}, 
            {'value':'89','label': 'Yonne'}, 
            {'value':'90','label': 'Territoire de Belfort'},
            {'value':'91','label': 'Essonne'}, 
            {'value':'92','label': 'Hauts-de-Seine'}, 
            {'value':'93','label': 'Seine-Saint-Denis'}, 
            {'value':'94','label': 'Val-de-Marne'}, 
            {'value':'95','label': 'Val-d\'Oise'},
            {'value':'971','label': 'Guadeloupe'}, 
            {'value':'972','label': 'Martinique'}, 
            {'value':'973','label': 'Guyane'}, 
            {'value':'974','label': 'La Réunion'}, 
            {'value':'975','label': 'Saint-Pierre-et-Miquelon'},
            {'value':'976','label': 'Mayotte'},
            {'value':'977','label': 'Saint-Barthélémy'},
            {'value':'978','label': 'Saint-Martin'},
            {'value':'986','label': 'Wallis-et-Futuna'},
            {'value':'987','label': 'Polynésie française'},
            {'value':'988','label': 'Nouvelle-Calédonie'},  
        ],     
         value='01',
         style = { 'width': '48%'},
    ),
    dcc.Graph(id='department-dropdown', style = {'display': 'inline-block', 'width': '48%'}),
    
    
# la charte affichant la mortalité par département
   
    dcc.Graph(
        id='carte',
        figure=fig_carte,
        style = {'display': 'inline-block', 'width':'48%'}
    ),   
],
)

#callback for the dropdown graph of the global hospitalisation

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('sexe-slider', 'value'))
def update_figure(selected_sexe):
    df2= df[df.sexe == selected_sexe]
    df2=df2[['hosp','rea','rad','dc']].groupby(df2['jour']).sum()
    df2.reset_index(inplace=True)

    fig = px.line(df2, x="jour", y=['hosp','rea'], 
           labels={'value':'Total', 'jour':''})


    fig.update_layout(transition_duration=500)

    return fig

# callback for the dropdown graph of hospitalisation per department
@app.callback(
    Output('department-dropdown', 'figure'),
    Input('mydrop', 'value'))
def update_figure(value):
    df_tot=df.query("sexe==0")
    df_dep= df_tot.loc[df_tot['dep'] == value]
    
    fig = px.line(df_dep, x="jour", y=['hosp','rea','dc'],
           labels={'value':'Total', 'jour':''})

    return fig

#graphique vaccination
@app.callback(Output('graph_vacc','figure'), [Input('reg','value')])
def cb(value):
    value=value if value else 1
    df_reg=df_tot_vacc.query('reg == @value')
    return px.line(df_reg, x='jour', y="n_cum_dose1", height=400,labels={'n_cum_dose1':'Total première dose', 'jour':'date'})

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)