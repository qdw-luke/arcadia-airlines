import pyodbc
import csv 
import os
from collections import namedtuple
import datetime
from string import Template 

data_paths = [os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_1.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_2.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_3.csv'), os.path.join(os.pardir,'randomdata','Origin_and_Destination_Survey_DB1BMarket_2015_4.csv')]
out_path =  os.path.join(os.pardir,'randomdata','Output1.csv')
states = []
#odbc_connection_string = 'Driver={SQL Server Native Client 11.0};Server=localhost;Database=airlines;Trusted_Connection=yes;'
data_sums = {}
origins = {}
destinations = {}
avg_tup = namedtuple('avg_tup', ['TotalFare', 'TotalTickets', 'AvgFare'])
insert_template = Template("""
INSERT INTO [dbo].[routes]
           ([AirportGroup]
           ,[OriginAirportCode]
           ,[Origin]
           ,[Destination]
           ,[DestAirportCode]
           ,[Fare]
           ,[Passengers]
           ,[Miles])
		VALUES ('$AirportGroup', '$OriginAiportCode', '$Origin', '$Destination', '$DestAirportCode', '$Fare', '$Passengers', '$Miles')
		"""
		)
routes = []

cnxn = pyodbc.connect(DSN='airlines')

cursor = cnxn.cursor()

for data_path in data_paths:
	print data_path 
	with open(os.path.join(data_path)) as csvfile:
		reader = csv.DictReader(csvfile, doublequote=False)
		totalrows = 0
		for x in reader:
			x_dic = x
			s_pair = x_dic['OriginStateName'] + ':' + x_dic['DestStateName']
			insert_string = insert_template.substitute(AirportGroup=x_dic['AirportGroup'], OriginAiportCode=x_dic['Origin'], Origin=x_dic['OriginStateName'], Destination=x_dic['DestStateName'], DestAirportCode=x_dic['Dest'], Fare=x_dic['MktFare'], Passengers=x_dic['Passengers'], Miles=x_dic['MktMilesFlown'])
			cursor.execute(insert_string)
			cursor.commit()

# cnxn = pyodbc.connect(odbc_connection_string)

# cursor = cnxn.cursor()

# for key in data_sums.keys():
# 		route_total, route_tix, route_avg = data_sums[key]
# 		origin = origins[key]
# 		destination = destinations[key]
# 		cursor.execute("INSERT INTO dbo.data_sums(AirportGroup, Origin,Destination, TotalFare, TotalTickets, AvgFare) VALUES ?, ?, ?, ?, ?, ?", key, origin, destination, route_total, route_tix, route_avg)
# 		#row_out = {'StatePair':key, 'OriginState':origin, 'DestState':destination, 'TotalFare':route_total, 'TotalTickets':route_tix, 'AvgFare':route_avg}
# 		#writer.writerow(row_out)