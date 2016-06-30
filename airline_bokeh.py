from math import pi
import os
import csv 

from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure, show, output_file

data_path = os.path.join(os.curdir, 'data', 'Output1.csv')
route_data = []
states = []
origins = []
destinations = []
colors = []
rates = []

color_set = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
          "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]



with open(os.path.join(data_path)) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		route_data.append(row)

for route in route_data:
	states.append(route['OriginState'])
	origins.append(route['OriginState'])
	destinations.append(route['DestState'])
	rates.append(float(route['AvgFare']))
	colors.append(color_set[min(int(float(route['AvgFare']))/100, 8)])
	#print min(int(float(route['AvgFare']))/100, 8)


states = set(states)
states = list(states)
states.sort()



source = ColumnDataSource(
    data=dict(origin=origins, destination=destinations,  rate=rates)
)


TOOLS = "hover,save,pan,box_zoom,wheel_zoom"

p = figure(title="State to State Fares",
           x_range=list(states), y_range=list(states),
           x_axis_location="above", plot_width=1000, plot_height=800,
           tools=TOOLS)



p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "9pt"
p.axis.major_label_standoff = 4
p.xaxis.major_label_orientation = pi/3


p.rect("origin", "destination", 1, 1, source=source,
       color=colors, line_color=None)

p.select_one(HoverTool).tooltips = [
    ('Origin', '@origin'),
    ('Destination', '@destination'),
    ('Fare', '@rate')
]

output_file('routes.html', title="Airline Routes  example")

show(p)