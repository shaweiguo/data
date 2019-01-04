# -*- coding: UTF-8 -*-

from bokeh.layouts import widgetbox
from bokeh.models import Slider, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
from numpy.random import random

# define the points that create the line plot
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [2, 3, 4, 5, 6, 7, 8, 9, 10]

data_points = ColumnDataSource(
    data={
        'x': x,
        'y': y,
    })

# Create the plot
plot = figure(title="Random line plot generator")
plot.line(x='x', y='y', source=data_points, color='red')

# Create the slider widget
slider_widget = Slider(start=0, end=100, step=1, value=10)


# Define the callback function
def callback(attr, old, new):
    points = slider_widget.value
    data_points.data = {
        'x': random(points),
        'y': random(points),
    }


slider_widget.on_change('value', callback)


# Create a layout for the application
# slider_layout = widgetbox(slider_widget1, slider_widget2, slider_widget3)
layout = row(slider_widget, plot)

# Add the slider widget to the application
curdoc().add_root(layout)
