#Welcome to Arcadia Airlines!

:airplane:

*We hope you are getting excited for the datathon coming up on August 19. To help get you prepared, we have put together four challenging implementation of the same data visualization project involving analyzing domestic US airfares. It may not be healthcare related but it should be a lot of fun.*

##Research Question

**How much does it cost to fly from one US state to another? Which is the most expensive pair of states to fly between?**

##Data Source. 
The [Airline Origin and Destination Survey](http://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125) is a government database that is based on a random 10% sample of all domestic airline tickets sold. It includes detail about the number of passengers, the itinerary (if it has stops), miles traveled and the airfare. The 4 files for 2015 (avail at the link) are 5.4gb and contain 14.3 Million Records. 

if you want the raw data you will have to download it from that link. I have summarized the data into data/Output1.csv which is much smaller and is laid out as follows:

|StatePair|OriginState|DestState|TotalFare|TotalTickets|AvgFare|
|---------|-----------|---------|---------|------------|-------|
|This is a pairing of the origin and desintation states to make a unique identifier for the row as in 'New York:California'.| Name of the origin state| Name of destination state| the sum of all the fare tickets in the files. | Some of how many tickets were found in the files| Average calculated as Total Tickets/ Total Fare. |


Each of the examples included work on the Output1.csv file. but i have also included a file that will work with the raw data if you are interested. The raw data may be accessed from the link above. 

##Use Case 1: Excel
We make fun of excel with its silly limits but it can actually do a lot.  Open the file data/"ArcadiaAirline Analysis.xlsx" and take a look. 

The worksheet output1 is exactly a copy of the csv data. the diagram is created from using the TRANSPOSE function and each cell is populated with a VLOOKUP. 

Some fancy formatting and then we got it. 

##Use Case 2: Sql Server Reporting Services

SQL Server comes bundled with BI package called Sql Server Reporting Services (SSRS). While we don't have access to the latest version, SSRS does have some robust tools and when paired with SQL server it actually was very easy to make this visualization. First some quick prerequisites: 

* You will need SQL Server Developer edition installed along with Sql Server Reporting Services. 
* You will also need [Sql Server Data tools](https://msdn.microsoft.com/en-us/library/mt204009.aspx) which is an add-on to visual studio 

If you have everything running, feel free to open ssrs/ArcadiaAirlineReporting/ArcadiaAirlineReporting.sln

But before you edit and run the report you will need to load the data so skip down to Loading the Data at the bottom. 

##Use case 3: Python Bokeh

So this is the most technical of the use cases. [Bokeh](http://bokeh.pydata.org/en/latest/) is one of 15 python libraries that are in the pantheon of amazing tools for data science. It provides a rich data visualization libary very much like [D3](https://d3js.org/) but it offers some differences that may make it easier to use because you don't need to directly interface with the DOM or frankly learn javascript. 

Prerequisites for Use Case 3: 
 
* You will need python installed on your machine. You have some choices here. There is the offical [Python for Windows](https://www.python.org/downloads/release/python-2712/) distribution. You may also consider the [Anaconda](https://www.continuum.io/downloads) distrubtuion which has several packages already included and is optimized for Data Science. I don't have anaconda and the instructions below would be slightly different using `conda` as opposed to standard python tools. Please install python 2.7 rather than python 3. Although python 3 is faster it is not backward compatible and some of this code may not work. 
* open a console or command line and navigate to a directory where you want to do this work. 
* checkout this package using git:
`git clone 



