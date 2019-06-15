import folium
import pandas

map = folium.Map(location=[38.58,-99.09], zoom_start = 3) # it will start the map at a certain position

data = pandas.read_csv("usa_volcano.txt") # pandas will allow to read and use the info in the txt file

name = list(data["NAME"])   # The list will have all the volcano names in the txt file
lat = list(data["LAT"])     # The list will store the latitude coordinates in the txt file
lon = list(data["LON"])     # The list will store the longitude coordinates in the txt file
elev = list(data["ELEV"])   # The list will store the elevations in the txt file
type = list(data["TYPE"])   # The list will store the types in the txt file

usa_volcano = folium.FeatureGroup(name = "U.S.A. Volcanoes") # this layer will store all markers of volcanoes in the txt file
pop = folium.FeatureGroup(name = "World Population") # this layer will store the population inforamtion from the json file

# this function will be used to distinguish the different elevations from the different volcanoes
def elevation_color(elevation):
    if elevation < 1000:
        return 'blue'
    elif 1000 <= elevation < 2000:
        return 'darkblue'
    elif 2000 <= elevation < 3000:
        return 'purple'
    else:
        return 'darkpurple'

for n,lt,ln,el,ty in zip(name, lat, lon, elev, type):
    #volcano.add_child(folium.Marker(location=[lt,ln], popup=str(el) + "m \nType: " + ty, tooltip = n, icon = folium.Icon(color = elevation_color(el))))

    usa_volcano.add_child(folium.CircleMarker(location=[lt,ln], radius = 6, popup=str(el) +"m \n Type: " + ty, tooltip = n, fill_color = elevation_color(el), color = 'grey', fill_opacity = 0.9))

# this will access the json file, and will use properties and pop2005 to color code countries based on their population
pop.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x:{'fillColor':'darkgreen' if x['properties']['POP2005'] < 10000000
else 'beige' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(pop)
map.add_child(usa_volcano)
map.add_child(folium.LayerControl())   # This will store pop and volcano as different layers that can be turned on and off in the HTML file
map.save("Map1.html")           # This saves the map as an HTML file called Map1
