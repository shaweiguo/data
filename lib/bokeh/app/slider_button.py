# -*- coding: UTF-8 -*-

# from bokeh.layouts import widgetbox
from bokeh.models import Button, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
from numpy.random import random, normal
import numpy as np

# Create data for plot
initial_points = 500
data_points = ColumnDataSource(
    data={
        'x': random(initial_points),
        'y': random(initial_points),
    })

# Create the plot
plot = figure(title="Data change application")
plot.diamond(x='x', y='y', source=data_points, color='red')

# Create the button widget
button_widget = Button(label='Change Data')


# Define the callback function
def callback():
    # New y values
    y = np.cos(initial_points) + random(initial_points)
    data_points.data = {
        'x': random(initial_points),
        'y': y,
    }


button_widget.on_click(callback)


# Create a layout for the application
# slider_layout = widgetbox(slider_widget1, slider_widget2, slider_widget3)
layout = row(button_widget, plot)

# Add the slider widget to the application
curdoc().add_root(layout)
