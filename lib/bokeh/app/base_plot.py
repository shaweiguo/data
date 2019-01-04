from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import pandas as pd

df = pd.read_csv('all_stocks_5yr.csv')
df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.strftime('%Y'))

data = ColumnDataSource(data={
    'high': df[df['date'] == '2013'].high,
    'low': df[df['date'] == '2013'].low,
    'open': df[df['date'] == '2013'].open,
    'close': df[df['date'] == '2013'].close,
    'volume': df[df['date'] == '2013'].volume,
    'Name': df[df['date'] == '2013'].Name
})

xmin, xmax = min(df.high), max(df.high)
ymin, ymax = max(df.volume), max(df.volume)

plot = figure(title='成交量/最高价', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))
plot.diamond(x='high', y='volume', source=data)
plot.xaxis.axis_label = '2013年最高价'
plot.yaxis.axis_label = '2013年成交量'

curdoc().add_root(plot)
curdoc().title = '股票成交量和最高价'
