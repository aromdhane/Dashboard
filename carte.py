import geopandas as gpd
import pandas as pd
import plotly.express as px

df = pd.read_csv("donnees-hospitalieres-covid19-2021-02-18-19h03.csv", delimiter=';')
print(df.head())

sf = gpd.read_file('departements-version-simplifiee.geojson')


dep_to_check = set(sf.code.unique())
print(dep_to_check)
print(sf)
df = df.loc[df.dep.isin(dep_to_check) == True]


fig = px.choropleth_mapbox(df, geojson=sf, color="rea",
                           locations="dep", featureidkey="properties.code",
                           center={"lat": 46.22, "lon": 2.21},
                           mapbox_style="carto-positron", zoom=5, range_color=[0, 500])

fig.show()