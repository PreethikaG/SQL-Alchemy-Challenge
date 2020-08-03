# Climate Analysis and Exploration - Surfs Up!

# Overview:

In this project, I used Python ,Matplotlib and SQLAlchemy to do a basic climate analysis and data exploration of climate database and render using FLASK API routes.

# Database connection :

I used sqlite and SQLAlchemy ORM for database interactions. Used `automap_base()` to reflect the tables in to classes and use them in code for manipulation by saving a reference to those classes. There were two tables 'Station'(which had details of Station ID,name,etc) and 'Measurement'(which had details of precipation value for each station for aparticular period of time). 

# Analysis -

# 1. Precipitation Analysis:
Calculated the date of the last data point and used it as reference to read the last 12 months of precipitation data from the 'Measurement' table. 
The 'filter' function was used to filter the data based on the date range needed.
Loaded the results in to a pandas dataframe and set the index to the date column.
A basic summary statistics table was created .
Used Pandas to plot the data for visually representing it.

# 2. Station Analysis:
A basic analysis on 

* Total number of stations

* The most active stations

* Listing the stations and observation counts in descending order

* Station has the highest number of observations

*  Retrieval of the last 12 months of temperature observation data (TOBS) and filtering by the station with the highest number of observations.

A query was written using sqlalchemy for each of the above listed items. Used filter,groupby,orderby, aggregating functions like sum,count,min,max,avg,etc
for getting the required result.

Loaded the results in to Pandas dataframe and plotted a histogram

# Climate App using FLASK -

Designed a Flask API based on the queries I developed. Following are the routes of the API.

# Routes

* `/`
Home page that lists all available routes.

* `/api/v1.0/precipitation`
Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
Return the JSON representation of the dictionary.

* `/api/v1.0/stations`
Return a JSON list of all stations from the dataset.

* `/api/v1.0/tobs`
Query the dates and temperature observations of the most active station for the last year of data.
Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.



