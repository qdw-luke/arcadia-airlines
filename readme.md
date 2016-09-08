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
We make fun of excel with its silly limits but it can actually do a lot.  Open the file "ArcadiaAirline Analysis.xlsx" and take a look. 

The worksheet output1 is exactly a copy of the csv data. the diagram is created from using the TRANSPOSE function and each cell is populated with a VLOOKUP. 

Some fancy formatting and then we got it. 

##Use Case 2: Sql Server Reporting Services

SQL Server comes bundled with BI package called Sql Server Reporting Services (SSRS). While we don't have access to the latest version, SSRS does have some robust tools and when paired with SQL server it actually was very easy to make this visualization. First some quick prerequisites: 

* You will need SQL Server  installed along with Sql Server Reporting Services. 
* You will also need [Sql Server Data tools](https://msdn.microsoft.com/en-us/library/mt204009.aspx) which is an add-on to visual studio 

Both of these are bundled in the express edition which you can download from microsoft. 

If you have everything running, feel free to open ssrs/ArcadiaAirlineReporting/ArcadiaAirlineReporting.sln

But before you edit and run the report you will need to load the data so skip down to Loading the Data at the bottom. 

You can preview the report right in Visual Studio but also you can upload it here http://lshulman-pc/Reports/ of course put your own Computer in there. 

##Use case 3: Python Bokeh

So this is the most technical of the use cases. [Bokeh](http://bokeh.pydata.org/en/latest/) is one of 15 python libraries that are in the pantheon of amazing tools for data science. It provides a rich data visualization libary very much like [D3](https://d3js.org/) but it offers some differences that may make it easier to use because you don't need to directly interface with the DOM or frankly learn javascript. 

Prerequisites for Use Case 3: 
 
* You will need python installed on your machine. You have some choices here. There is the offical [Python for Windows](https://www.python.org/downloads/release/python-2712/) distribution. You may also consider the [Anaconda](https://www.continuum.io/downloads) distrubtuion which has several packages already included and is optimized for Data Science. I don't have anaconda and the instructions below would be slightly different using `conda` as opposed to standard python tools. Please install python 2.7 rather than python 3. Although python 3 is faster it is not backward compatible and some of this code may not work. 
* open a console or command line and navigate to a directory where you want to do this work. 
* checkout this package using git:
`git clone https://github.com/qdw-luke/arcadia-airlines.git`
* go into the project directory
* make sure you have virtualenv installed virtualenv helps keep your python projects from stepping on each other. enter `pip install virtualenv` if pip doesn't work start googling. use [this page](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for help
* with virtualenv install you now initialize the environement. This wil create a folder to contain packages specific to the environment. 
`virtualenv env`
* if all went well, we will now activate the virtual environement. 
windows: `.\env\Scripts\activate` 
Linux/Mac: `source ./env/Scripts/activate`
* Now with our own fresh environement we get to install pre-requisite packages which are listed in an inventory. If you are familar with ruby this the same as gems. 
`pip install -r requirements.txt`
* Assuming you got no errors thus far lets go ahead and just run the app: `python airline_bokeh.py` this should run and open a page in your browser. You are now set-up to play with it. 

The bokeh packages have a few parts. airline_bokeh.py controls the creation of the visual and outputs it as a static html page called routes.html. 

alternativaly we can use the interactive Notebook to look at the graph. These are called Jupyter Notebooks. 

run `jupyter notebook`

a browser should open and then select ArcadiaAirlines.ipynb

Alternatively, you can view the output at the below: 
http://nbviewer.jupyter.org/github/qdw-luke/arcadia-airlines/blob/master/ArcadiaAirlines.ipynb

##Use Case 4: QlikView

So QlikView is a commercial BI platform that has really wide-usage in many industries. The personal edition is free so you can go ahead and download it at [Qlikview](http://www.qlik.com/try-or-buy/download-qlikview). They will make you register and they will SPAM you so be careful. Qlik personal is fully functional except they will not let you share files. So you go ahead and open the ArcadiaAirlines.qvw file thorugh which you will take ownership of it. 

After this point, the file will be yours so be aware if you open someone elses file it may lock you out of other files created by other users. 

You will notice QlikView is the only system where I actually couldn't colors to work. so theres a challenge. 

##Loading the data
If you scrolled this far down, it probably means you wanted to work with the raw data. So go ahead and download the files from [Airline Origin and Destination Survey](http://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125) and get them saved somewhere.

There are two scripts for data loading. 

1. `datafile.py`: this python script generates a CSV with each origin/destination pair and the total tickets, total paid fare, and Avg fare. the resulting CSV should be about 2704 lines long which is exactly 52^2. Now why 52, well not every state has an airport and not every state actually flies to every other state so the exact number will vary based on the files you are using. also there are several non-state entries such as US Pacific Territories, which I presume to be guam. 

check out the top section of `datafile.py`. You will need update the variables for `data_paths` which is a list of all the files you want to load and  `out_path` which is the name of the output file that you want. note that we are using `os.path.join` so you do not need to explicitly state the directory just seperate each component with a comma. this helps ensure compatability in multiple systems. for instance if you wanted to start in your home directory and navigate to a file as in '.\Documents\Arcadia\Somefile.docx' you express that as `os.path.join(os.curdir,'Documents','Arcadia','Somefile.docx')`

Running the datafile creates a python dictionary where each key is a unique combo of origin and destination and the value is a tuple with the data. 

Data file takes about 5-8  min to load. 


2. `airlines_sql_load.py`: 
This file simply loads the data from a flat and sends it off sql to server. This won't work on non-windows machines. Make sure you set-up a odbc DSN and put the parameter in the connector on line 31. 




##Reading List

* https://github.com/fasouto/awesome-dataviz Great Resource
* http://blog.revolutionanalytics.com/2016/08/five-great-charts-in-5-lines-of-r-code-each.html Great R Examples

