import pandas, folium

# import data as dataframe
data = pandas.read_excel('data.xlsx')

# split data of TYPE column in list
data["TYPE"] = data["TYPE"].str.split(',')

# explode data in multiple rows
data_multiple_rows = data.apply(pandas.Series.explode)

lat = list(data_multiple_rows['LAT'])
lon = list(data_multiple_rows['LON'])
place = list(data_multiple_rows['NAME'])
charge = list(data_multiple_rows['CHARGE'])
acticity = list(data_multiple_rows['TYPE'])
link = list(data_multiple_rows['LINK']) 

# create map and overlay`s
map = folium.Map(location=[56.949533,24.172519], tiles=None)
folium.TileLayer('openstreetmap',overlay=False).add_to(map)
folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='google',
    name='Google street view',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(map)
folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='google',
    name='google Areal',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(map)

atu = set(acticity)

for i in atu:
    fg = folium.FeatureGroup(name=i, show=False, collapsed=False)
    for ac, lt, ln, pl, ch, lk in zip(acticity, lat, lon, place, charge, link):
        if ac == i:
            fg.add_child(folium.Marker(location=[lt, ln], popup=f"{pl}\n Maksa:{ch} \n<a href= http://{lk} >{lk}</a>", icon=folium.Icon(icon='star', color='red')))
    map.add_child(fg)

map.add_child(folium.LayerControl())
map.save("map.html")
