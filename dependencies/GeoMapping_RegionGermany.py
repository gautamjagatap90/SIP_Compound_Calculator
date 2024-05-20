
import socket
# Set a timeout for network connections (e.g., 0 seconds to block)
# socket.setdefaulttimeout(0)
# Reset the socket timeout to the system default
# socket.setdefaulttimeout(None)

import os
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go

# Set the working directory
os.chdir(r"\\quintiles.net\Enterprise\Sites\DEFFM\Depts\Consulting\02 Projects\04 Internal Projects\Webcrawler\INDIA TEAM\00_Standard Scripts\002_GeoMapRegionOverlay_20240113")
print(os.getcwd())

# Load datasets
data = pd.read_excel('output.xlsx')
lat_long_data = pd.read_excel('LAT_LONG_GERMANY_PLZs.xlsx')
population_data = pd.read_excel('germany_population.xlsx')

# Merge datasets for latitude and longitude
data['PLZ'] = data['PLZ'].astype(str)
lat_long_data['Postal Code'] = lat_long_data['Postal Code'].astype(str)
merged_phy_data = pd.merge(data, lat_long_data[['Postal Code', 'lat', 'long']], left_on='PLZ', right_on='Postal Code', how='left')


# Create hover text for physician locations (assuming 'full_name' column exists)
merged_phy_data['hover_text'] =merged_phy_data['hover_text'] = merged_phy_data['vorname_list'] + ' ' + merged_phy_data['nachname_list']
  # Replace with actual column name


# Read Germany shapefile for states
germany_states = gpd.read_file('Germany Shape File\DEU_adm1.shp')

# Merge the population data with the shapefile data
germany_states = germany_states.merge(population_data, left_on='NAME_1', right_on='State Name')

# Creating an interactive map with Plotly
fig = go.Figure()

# State/Region Coloring - Choroplethmapbox for state boundaries
fig.add_trace(go.Choroplethmapbox(
    geojson=germany_states.geometry.__geo_interface__,
    locations=germany_states.index,
    z=germany_states['Population'],
    text=germany_states['State Name'],
    colorscale="blues",
    marker_opacity=0.5,
    marker_line_width=2,
    marker_line_color='gray'
))

# PHY Positions - A Segment
fig.add_trace(go.Scattermapbox(
    lat=merged_phy_data[merged_phy_data['Phy Number']>=5]['lat'],
    lon=merged_phy_data[merged_phy_data['Phy Number']>=5]['long'],
    mode='markers',
    marker=go.scattermapbox.Marker(size=8, color='orange', opacity=1),
    text=merged_phy_data[merged_phy_data['Phy Number']>=5]['hover_text'],
    hoverinfo='text'
))


# PHY Positions - B segment
fig.add_trace(go.Scattermapbox(
    lat=merged_phy_data[merged_phy_data['Phy Number']<5]['lat'],
    lon=merged_phy_data[merged_phy_data['Phy Number']<5]['long'],
    mode='markers',
    marker=go.scattermapbox.Marker(size=8, color='Brown', opacity=1),
    text=merged_phy_data[merged_phy_data['Phy Number']<5]['hover_text'],
    hoverinfo='text'
))
# National Boundary
##########################

# Read Germany shapefile for national boundary
germany_national = gpd.read_file('Germany Shape File\DEU_adm0.shp')

import json
# Convert the geometry to GeoJSON format
geojson_national = json.loads(germany_national.to_json())

# Extract the coordinates from the GeoJSON
# Assuming the national boundary is the first feature in the GeoJSON
coords = geojson_national['features'][0]['geometry']['coordinates']

# Since the national boundary might be a MultiPolygon, we handle it accordingly
lon, lat = [], []
for part in coords:
    if isinstance(part[0][0], list):  # This is for MultiPolygon
        for segment in part:
            lon += [p[0] for p in segment] + [None]  # Adding None to break the line
            lat += [p[1] for p in segment] + [None]
    else:  # This is for a simple Polygon
        lon += [p[0] for p in part] + [None]
        lat += [p[1] for p in part] + [None]

# Add national border to the map
national_border = go.Scattermapbox(
    lon=lon,
    lat=lat,
    mode='lines',
    line=go.scattermapbox.Line(color='black', width=1),
    hoverinfo='none'
)
fig.add_trace(national_border)


# Map Setting
###################

# Map layout settings
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=5,
    mapbox_center={"lat": 51.1657, "lon": 10.4515},
    title_text="Germany Map: States with National Border, Major Cities, and Physician Locations",
    margin={"r":0, "t":50, "l":0, "b":0}
)



fig.show()


# Save the interactive map as an HTML file
# fig.write_html("germany_interactive_map.html")






#
# XML TO GEOJSON CONVERTER
#

# import subprocess

# subprocess.run("conda install GDAL", shell=True, check=True)


# # Specify the input XML file and the output GeoJSON file
# input_xml_file = r'C:\Users\u46859\OneDrive - IQVIA\Desktop\GeoMapping\test.xml'
# output_geojson_file = 'output.geojson'

# # Specify the path to ogr2ogr executable
# ogr2ogr_executable = r'C:\path\to\ogr2ogr.exe'  # Replace with the actual path

# # Construct the ogr2ogr command as a list
# ogr2ogr_command = [
#     ogr2ogr_executable,  # Path to ogr2ogr executable
#     '-f', 'GeoJSON',     # Specify the output format as GeoJSON
#     output_geojson_file, # The output GeoJSON file path
#     input_xml_file       # The input XML file path
# ]

# # Execute the ogr2ogr command
# try:
#     subprocess.run(ogr2ogr_command, check=True)
#     print(f'Successfully converted {input_xml_file} to {output_geojson_file}')
# except subprocess.CalledProcessError as e:
#     print(f'Error running ogr2ogr: {e}')






