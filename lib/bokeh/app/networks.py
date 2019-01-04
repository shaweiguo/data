# -*- coding: UTF-8 -*-

import math
from bokeh.io import show, output_file
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral10
from bokeh.plotting import figure

total_nodes = 10
node_points = list(range(total_nodes))
print(node_points)

# Create the plot
plot = figure(x_range=(-1.1, 1.1), y_range=(-1.1, 1.1))

network = GraphRenderer()
network.node_renderer.data_source.add(Spectral10, 'color')
network.node_renderer.data_source.add(node_points, 'index')
network.node_renderer.glyph = Oval(height=0.2, width=0.3, fill_color='color')
network.edge_renderer.data_source.data = dict(start=[1]*total_nodes, end=node_points)

node_circumference = [node*2*math.pi/10 for node in node_points]
x = [math.cos(circum) for circum in node_circumference]
y = [math.sin(circum) for circum in node_circumference]
print('x:')
print(x)
print('y')
print(y)

network_layout = dict(zip(node_points, zip(x, y)))
print('network_layout:')
print(network_layout)

network.layout_provider = StaticLayoutProvider(graph_layout=network_layout)

plot.renderers.append(network)
output_file('network.html')
show(plot)
