# -*- coding: UTF-8 -*-

import numpy as np
import random
from bokeh.io import show, output_file
from bokeh.plotting import figure

# Creating an array for the points along the x and y axes
array_x = np.array([1, 2, 3, 4, 5, 6])
array_y = np.array([5, 6, 7, 8, 9, 10])

# Creating a line plot
plot = figure(output_backend='webgl')
plot.line(array_x, array_y)

# Output the plot
output_file('webgl.html')
show(plot)
