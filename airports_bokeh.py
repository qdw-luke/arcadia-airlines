from math import pi
import os
import csv 
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure, show, output_file, save
import pyodbc
import numpy as np
from bokeh.sampledata.us_states import data as states

data_path = os.path.join(os.curdir, 'data', 'Output1.csv')
coord_path = os.path.join(os.curdir, 'data', 'airports.csv')

origins = {}
coord_data = {}


state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]




cnxn = pyodbc.connect(DSN='airlines')

cursor = cnxn.cursor()

cursor.execute("""
	SELECT OriginAirportCode, SUM(Passengers) as Passengers from dbo.routes
group by OriginAirportCode """)

with open(os.path.join(coord_path)) as csvfile:
	reader = csv.reader(csvfile, quotechar='"')
	for row in reader:
		if row[4] is not None:
			coord_data[row[4]] = float(row[6]), float(row[7])

for row in cursor.fetchall():
	if row[0] not in origins.keys():
		origins[row[0]] = row[1]
	else:
		origins[row[0]] = origins[row[0]] + row[1]

airports = sorted(origins.keys())

names = []
lats = []
longs = []
radius = []

# for airport in airports:
# 	if airport in coord_data.keys():
# 		names.append(airport)
# 		latitude, longitude = coord_data[airport]
# 		if latitude <= 0:
# 			latitude = abs(latitude) + 90
# 		lats.append(latitude)
# 		if longitude <= 0:
# 			longitude = 180 + longitude
# 		else:
# 			longitude = longitude + 180
# 		longs.append(longitude)
# 		radius.append(origins[airport])

for airport in airports:
	if airport in coord_data.keys():
		names.append(airport)
		latitude, longitude = coord_data[airport]
		lats.append(latitude)
		longs.append(longitude)
		radius.append(origins[airport])



radius_max = max(radius)
radius_min = min(radius)
print radius_max, radius_min
std_radius = [(((rad - radius_min)/(radius_max - radius_min))*40) for rad in radius]


N = len(names)

x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = ["#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]


source = ColumnDataSource(
    data=dict(names=names, lats=lats,  longs=longs, radius=std_radius, people=radius, colors=colors)
)


TOOLS = "hover,save,pan,box_zoom,wheel_zoom"

p = figure(title="AirportPlot", plot_width=1080, plot_height=540,
           tools=TOOLS)


p.circle(x="longs", y="lats", size="radius", source=source,
                  color="colors", fill_alpha=0.2, line_width=2)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)


p.select_one(HoverTool).tooltips = [
    ('Airport', '@names'),
    ('Lat', '@lats'),
    ('long', '@longs'),
    ('People','@people')
]


output_file('airports.html', title="Airline Routes  example")


save(p)