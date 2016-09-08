import csv 
import os
from collections import namedtuple
import datetime


data_paths = [os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_1.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_2.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_3.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_4.csv')]
out_path =  os.path.join(os.pardir,'randomdata','Output2.csv')
states = []
data_sums = {}
origins = {}
destinations = {}
avg_tup = namedtuple('avg_tup', ['TotalFare', 'TotalTickets', 'AvgFare'])

routes = []

for data_path in data_paths:
	print data_path 
	with open(os.path.join(data_path)) as csvfile:
		reader = csv.DictReader(csvfile, doublequote=False)
		for x in reader:
			x_dic = x
			s_pair = x_dic['OriginStateName'] + ':' + x_dic['DestStateName']
			if s_pair in data_sums.keys():
				route_total, route_tix, route_avg = data_sums[s_pair]
				route_total = route_total + float(x_dic['MktFare'])
				route_tix = route_tix + 1
				route_avg = route_total / route_tix
				data_sums[s_pair] = avg_tup(TotalFare=route_total, TotalTickets=route_tix, AvgFare=route_avg)
			else:
				data_sums[s_pair] = avg_tup(TotalFare=float(x_dic['MktFare']), TotalTickets=1, AvgFare=float(x_dic['MktFare']))
				origins[s_pair] = x_dic['OriginStateName']
				destinations[s_pair] = x_dic['DestStateName']


with open(out_path, 'wb') as csvfile:
	fieldnames = ['StatePair', 'OriginState', 'DestState', 'TotalFare', 'TotalTickets', 'AvgFare']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for key in data_sums.keys():
		route_total, route_tix, route_avg = data_sums[key]
		origin = origins[key]
		destination = destinations[key]
		row_out = {'StatePair':key, 'OriginState':origin, 'DestState':destination, 'TotalFare':route_total, 'TotalTickets':route_tix, 'AvgFare':route_avg}
		writer.writerow(row_out)

print len(origins.keys())

	# for dataval in reader:
	# 	if dataval['AirportGroup'] not in data_sums.keys():
	# 		data_sums[dataval['AirportGroup']] = float[dataval['MktFare']]
	# 	else:
	# 		data_sums[dataval['AirportGroup']] = data_sums[dataval['AirportGroup']] + float[dataval['MktFare']]







# ['ItinID', 'MktID', 'MktCoupons', 'Year', 'Quarter', 'OriginAirportID',
#  'OriginAirportSeqID', 'OriginCityMarketID', 'Origin', 
#  'OriginCountry', 'OriginStateFips', 'OriginState', 
#  'OriginStateName', 'OriginWac', 'DestAirportID', 
#  'DestAirportSeqID', 'DestCityMarketID', 'Dest', 
#  'DestCountry', 'DestStateFips', 'DestState', 
#  'DestStateName', 'DestWac', 'AirportGroup', 
#  'WacGroup', 'TkCarrierChange', 'TkCarrierGroup', 
#  'OpCarrierChange', 'OpCarrierGroup', 'RPCarrier',
#   'TkCarrier', 'OpCarrier', 'BulkFare', 'Passengers',
#    'MktFare', 'MktDistance', 'MktDistanceGroup', 
#    'MktMilesFlown', 'NonStopMiles', 'ItinGeoType',
#     'MktGeoType', '']