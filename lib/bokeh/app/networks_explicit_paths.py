# -*- coding: UTF-8 -*-

import math
from bokeh.io import show, output_file
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral10
from bokeh.plotting import figure

# Configure the number of nodes
total_nodes = 10
node_points = list(range(total_nodes))
print(node_points)

# Create the network
plot = figure(x_range=(-1.1, 1.1), y_range=(-1.1, 1.1))
network = GraphRenderer()

# Customize your network
network.node_renderer.data_source.add(node_points, 'index')
network.node_renderer.glyph = Oval(height=0.2, width=0.3, fill_color='green')
network.edge_renderer.data_source.data = dict(start=[1]*total_nodes, end=node_points)

# Render your network in 2-D space
node_circumference = [node*2*math.pi/10 for node in node_points]
x = [math.cos(circum) for circum in node_circumference]
y = [math.sin(circum) for circum in node_circumference]
network_layout = dict(zip(node_points, zip(x, y)))
network.layout_provider = StaticLayoutProvider(graph_layout=network_layout)

values = [value/100. for value in range(100)]


def quad_path(start, end, control, values):
    return [(1-value)**2*start + 2*(1-value)*control + value**2*end for value in values]


# Initialize empty lists to store the x and y co-ordinates
x_point, y_point = [], []

# Store the starting and ending points
x_start, y_start = network_layout[0]

# Create the set of co-ordinates for the quadratic path
values = [value/100. for value in range(100)]
for node in node_points:
    x_end, y_end = network_layout[node]
    x_point.append(quad_path(x_start, x_end, 0, values))
    y_point.append(quad_path(y_start, y_end, 0, values))

# Add the x and y co-ordinates of the quadratic path to the network
network.edge_renderer.data_source.data['xs'] = x_point
network.edge_renderer.data_source.data['ys'] = y_point

# Output the plot
plot.renderers.append(network)
output_file('quad_path.html')
show(plot)
