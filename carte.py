import geopandas as gpd
sf = gpd.read_file('departements-version-simplifiee.geojson')
print(sf.head())