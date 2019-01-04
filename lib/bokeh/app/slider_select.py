# -*- coding: UTF-8 -*-

# from bokeh.layouts import widgetbox
from bokeh.models import Select, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
from numpy.random import random, normal

# Create data for plot
initial_points = 500
data_points = ColumnDataSource(
    data={
        'x': random(initial_points),
        'y': random(initial_points),
    })

# Create the plot
plot = figure(title="Scatter plot distribution selector")
plot.diamond(x='x', y='y', source=data_points, color='red')

# Create the select widget
select_widget = Select(options=['uniform distribution', 'normal distribution'],
                       value='uniform distribution',
                       title='Select the distribution of your choice')


# Define the callback function
def callback(attr, old, new):
    if select_widget.value == 'uniform distribution':
        func = random
    else:
        func = normal
    data_points.data = {
        'x': func(size=initial_points),
        'y': func(size=initial_points),
    }


select_widget.on_change('value', callback)


# Create a layout for the application
# slider_layout = widgetbox(slider_widget1, slider_widget2, slider_widget3)
layout = row(select_widget, plot)

# Add the slider widget to the application
curdoc().add_root(layout)
