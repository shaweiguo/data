# -*- coding: UTF-8 -*-

from bokeh.layouts import widgetbox
from bokeh.models import Slider, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
from numpy.random import random

# Create data for the plot
initial_points = 500
data_points = ColumnDataSource(
    data={
        'x': random(initial_points),
        'y': random(initial_points),
    })

# Create the plot
plot = figure(title="随机散点图生成器")
plot.diamond(x='x', y='y', source=data_points, color='red')

# Create the slider widget
slider_widget = Slider(start=0, end=10000, step=10, value=initial_points,
                       title='Slide right to increase number of points')
# slider_widget1 = Slider(start=0, end=100, step=10, title='Single Slider 1')
# slider_widget2 = Slider(start=0, end=50, step=5, title='Single Slider 2')
# slider_widget3 = Slider(start=50, end=100, step=5, title='Single Slider 3')


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
