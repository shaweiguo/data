# -*- coding: UTF-8 -*-

from bokeh.sampledata import us_states
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool

# Create a copy of the USA data in our program
usa_data = us_states.data.copy()

# Delete the states that are out of interest
del usa_data['HI']
del usa_data['AK']

# Extract the latitude and longitude information
longitude = [usa_data[long]['lons'] for long in usa_data]
latitude = [usa_data[lat]['lats'] for lat in usa_data]

# Create the Hover Tool
hover_tool = HoverTool(tooltips=[
    ('Longitude', '@x'),
    ('Latitude', '@y')
])

# Create the  figure
plot = figure(title='美国最安全的三个州', tools=[hover_tool])

# Configure the borders of the states
plot.patches(longitude, latitude, line_color='red', line_width=2)

# Mapping the longitude and latitude information into lists
long_list = [-69.44, -72.57, -71.57]
lat_list = [45.25, 44.55, 43.19]

# Create the markers for the states
plot.diamond(long_list, lat_list, size=15, color='yellow')

# Output the plot
output_file('safe.html')
show(plot)
