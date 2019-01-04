# -*- coding: UTF-8 -*-

from bokeh.models import Select, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
import pandas as pd

# Read in the data
df = pd.read_csv('all_stocks_5yr.csv')

# Filtering for apple stocks
df_apple = df[df['Name'] == 'AAL']
data = ColumnDataSource(
    data={
        'x': df_apple['high'],
        'y': df_apple['low'],
        'x1': df_apple['volume']
    })

# print('plot')
# Create the plot
plot = figure(title="属性选择")
plot.diamond('x', 'y', source=data, color='red')

# Create the select widget
select_widget = Select(options=['low', 'volume'],
                       value='low',
                       title='Select a new y axis attribute')


# Define the callback function
def callback(attr, old, new):
    if new == 'low':
        data.data = {'x': df_apple['high'], 'y': df_apple['low']}
    else:
        data.data = {'x': df_apple['high'], 'y': df_apple['volume']}


select_widget.on_change('value', callback)


# Create a layout for the application
layout = row(select_widget, plot)

# Add the slider widget to the application
curdoc().add_root(layout)
