import folium
import pandas

map = folium.Map(location=[38.58, -99.09], zoom_start = 3) # folium.Map help generates a map that will serve as the output of the program

volcano_data = pandas.read_csv("japanese_volcano.txt")  # pandas will allow to use the data seperated by commas in the txt file
lat = list(volcano_data["LAT"])        # The list will contain all the Latitude coordinates
lon = list(volcano_data["LON"])        # The list will contain all the Longitude coordinates
name = list(volcano_data["NAME"])      # The list will contain all the names
elev = list(volcano_data["ELEV"])      # The list will contain the elevations
stat = list(volcano_data["STATUS"])    # The list will contain the status of the Volcanoes
type = list(volcano_data["TYPE"])      # The list will contain the type of volcano it they are
number = list(volcano_data["NUMBER"])  # The list will contain the volcano number that will be used for the popup link

# html is used to help format the popup in a marker, and will also help in having a link to more info about a volcano
html = """
<a href="https://volcano.si.edu/volcano.cfm?vn=%s" target="_blank">%s</a><br>
Height: %sm<br>
Type: %s
"""

# the method here will color code the volcanoes based on their elevation
def elevation_color(elevation):
    if elevation < 0:
        return 'cadetblue'
    elif 0 <= elevation < 1000:
        return 'blue'
    elif 1000<= elevation < 2000:
        return 'darkblue'
    elif 2000<= elevation < 3000:
        return 'purple'
    else:
        return 'darkpurple'

volcano = folium.FeatureGroup(name = "Japanese Volcanoes")  # This will have all the markers of the Volcanoes
pop = folium.FeatureGroup(name = "World Population")        # This will have the color coded country populations

for n, el, lt, ln, st, ty, num in zip(name, elev, lat, lon, stat, type, number):

    iframe = folium.IFrame(html = html % (str(num),n,el,ty), width = 150, height=100) # IFrame() is used to set up the popup with the name of the volcano being the link
    # this creates every CircleMarker() that is used for each volcano
    volcano.add_child(folium.CircleMarker(location=[lt,ln], radius = 6, popup = folium.Popup(iframe), tooltip = n, fill_color = elevation_color(el), color = 'grey', fill_opacity = 0.9))

# folium.GeoJson is used to help color code the countries based on population using the world.json values of [properties][POP2005]
pop.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(volcano)
map.add_child(pop)
map.add_child(folium.LayerControl()) # this will have two layers aside from the map, 1st layer is the volcanoes, 2nd layer is the world population
map.save("Map2.html") # map.save() saves the map as an html file as the output
