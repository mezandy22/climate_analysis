
# coding: utf-8

# In[232]:

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib
# from matplotlib import style
# style.use('fivethirtyeight')
# import matplotlib.pyplot as plt


# In[17]:

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")


# In[18]:

# Declare a Base using `automap_base()`
Base = automap_base()


# In[19]:

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)


# In[20]:

# Print all of the classes mapped to the Base
Base.classes.keys()


# In[21]:

# Assign the stations class to a variable called `stations`
stations = Base.classes.stations
stations


# In[22]:

# Assign the measurements class to a variable called `measurements`
measurements = Base.classes.measurements
measurements


# In[23]:

# To persist hawaii.sqlite database, we use a Session object
# A session is akin to a conversation between Python and SQL
# Define session
session = Session(bind=engine)


# In[28]:

# Use the session to query measurments table and display the first 5 locations
for row in session.query(measurements, measurements.tobs, stations.station).limit(5).all():
    print(row)


# In[33]:

# Use the session to query measurments table and display the first 5 locations
for row in session.query(stations, stations.station).all():
    print(row)


# # Climate Analysis and Exploration
# 
# Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
# 
# Travel Dates: 2017-04-18 to 2017-04-25

# ## Precipitation Analysis
# * Design a query to retrieve the last 12 months of precipitation data.
# * Select only the date and prcp values.
# * Load the query results into a Pandas DataFrame and set the index to the date column.
# * Plot the results using the DataFrame plot method.
# 

# In[362]:

import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np


# In[359]:

#checking most recent record date using the -1 indice
session.query(measurements.date)[-1]


# In[360]:


#https://stackoverflow.com/questions/546321/how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime
last_date = dt.date(2017, 8, 23)
last_date


# In[170]:

#testing the subtracting with relative delta
last_date-relativedelta(months=12)
# datetime.date(2011, 1, 31)


# In[171]:

# session.execute('SELECT * FROM measurements WHERE tobs = 65').fetchall()


# In[194]:

#build query for last 12 months of prcp data
#using the last_date datime variable and relativedelta in filter to get last 12 months
prcp_query = session.query(func.strftime(measurements.date), (measurements.prcp)).filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).all()

prcp_query


# In[208]:

#build query for last 12 months of prcp data
#using the last_date datime variable and relativedelta in filter to get last 12 months
#grouped by
prcp_gb_query = session.query(func.strftime(measurements.date), func.avg(measurements.prcp)).filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).group_by(measurements.date).all()

prcp_gb_query


# In[209]:

# #querying for dates in april
# for row in session.query(measurements, measurements.date).filter(func.strftime("%Y", measurements.date) == "2017").all():
#     print(row)


# In[233]:

#place data in pandasdataframe
# Plot the Results
prcp_gb_year = pd.DataFrame(prcp_gb_query, columns=['date', 'prcp'])
prcp_gb_year.set_index('date', inplace=True)
prcp_gb_year

# prcp_past_yr.groupby(['date'])['prcp'].mean()
prcp_gb_year.plot(kind = 'bar', rot='vertical')
#set number of ticks for x axis
#https://stackoverflow.com/questions/6682784/how-to-reduce-number-of-ticks-with-matplotlib
plt.locator_params(axis='x', nbins="8")
plt.tight_layout()
plt.show()

##need to show time span for xticks


# In[234]:

#precipitation descriptive statistics
prcp_gb_year['prcp'].describe()


# # Station Analysis
# * Design a query to calculate the total number of stations. 
# * Design a query to find the most active stations.
# * List the stations and observation counts in descending order
# 
# Which station has the highest number of observations?
# * Design a query to retrieve the last 12 months of temperature observation data (tobs).
# * Filter by the station with the highest number of observations.
# * Plot the results as a histogram with bins=12.
# ##### Clarification added by pavan on wed oct 18 8:35 pm
# * Choose the station with the highest number of temperature observations.
# * Query the last 12 months of temperature observation data for this station and plot the results as a histogram
# 

# In[317]:

#count of stations. 

total_stations_query = session.query(measurements.station).count()
total_stations_query

tot_stations_query = session.query(stations.station).count()
tot_stations_query


# In[351]:

#most active stations over the entire data set. Defaults to descending order of count
high_sta_obs = session.query(measurements.station, func.count(measurements.stations)).                group_by(measurements.station).order_by(measurements.tobs).all()
high_sta_obs


# In[352]:

#get station with max observations from the entire data set spanning all years
#key for itemgetter is set to 1 due to tobs being in position 1 and station being position 0
from operator import itemgetter
max(high_sta_obs,key=itemgetter(1))


# In[349]:

#Counting number of observations made by station in the last 12 months of data set
count_stn_obs_yr = session.query(measurements.station, func.count(measurements.station)).                filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).                group_by(measurements.station).order_by(measurements.tobs).all()

#only 7 stations had observations in the last year        
count_stn_obs_yr


# In[350]:

#get max observations from the past year
#key for itemgetter is set to 1 due to tobs being in position 1 and station being position 0
max(count_stn_obs_yr,key=itemgetter(1))


# In[335]:

#data of station with max observation over past 12 months USC00519397. 
USC00519397_obs_query = session.query(measurements.station, (measurements.tobs)).                filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).                filter(measurements.station=='USC00519397').                order_by(measurements.tobs).all()
USC00519397_obs_query


# In[336]:

station_tobs_yr = pd.DataFrame(USC00519397_obs_query, columns=['station', 'tobs'])
station_tobs_yr.head()


# In[347]:

#histogram using pandas hist

station_tobs_yr.hist(bins=12)
plt.title("Temp Frequency Stations USC00519397 - Past 12 Months")
plt.xlabel("Tempurature(F)")
plt.ylabel("Frequency")
# plt.tight_layout()
plt.show()


# # Temperature Analysis
# Travel Dates: 2017-04-18 to 2017-04-25
# 
# * Write a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d and return the minimum, average, and maximum temperatures for that range of dates.
# * Use the calc_temps function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e. use "2017-01-01" if your trip start date was "2018-01-01")
# * Plot the min, avg, and max temperature from your previous query as a bar chart.
#   * Use the average temperature as the bar height.
#   * Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr).
# 

# In[403]:

#creating calc_temps function

def calc_temps(start_date, end_date):
    
#     last_date = dt.date(2017, 8, 23)
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")

    max_temp = session.query(func.max(measurements.tobs)).                filter(measurements.date <= end_date1, measurements.date>= start_date1).all()
    max_temp = list(np.ravel(max_temp))
            
    avg_temp = session.query(func.avg(measurements.tobs)).                filter(measurements.date <= end_date1, measurements.date>= start_date1).all()
    avg_temp = list(np.ravel(avg_temp))
            
    min_temp = session.query(func.min(measurements.tobs)).                filter(measurements.date <= end_date1, measurements.date>= start_date1).all()
    min_temp = list(np.ravel(min_temp))
            
    return max_temp, avg_temp, min_temp

print(calc_temps('2017-04-18', '2017-04-25'))


# In[434]:

#creating calc_temps function and uses 1 query to return max, avg and min in 1 list.

def calc_temps(start_date, end_date):
    
#     last_date = dt.date(2017, 8, 23)
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")

    temp_data = session.query(func.max(measurements.tobs), func.avg(measurements.tobs), func.min(measurements.tobs)).                filter(measurements.date <= end_date1, measurements.date>= start_date1).all()
#     temp_data = list(np.ravel(temp_data))

    return temp_data

# print(calc_temps('2017-04-18', '2017-04-25'))

t_data = calc_temps('2017-04-18', '2017-04-25')

print(t_data)


# In[435]:

#Find max tempature found at each station in the last 12 months (tobs)
max_stn_temp_yr = session.query(measurements.station, func.max(measurements.tobs)).                filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).                group_by(measurements.station).order_by(measurements.tobs).all()

#only 7 stations had observations in the last year        
max_stn_temp_yr


# In[404]:

#plotting box plot for min, max and avg temps
fig, ax = plt.subplots()

x = range(len(t_data))
ax.boxplot(t_data, patch_artist=True)
ax.set_title('Temp Min, Max and Avg')
fig.tight_layout()
plt.show()
### END SOLUTION


# In[451]:



#plotting box plot for min, max and avg temps
fig, ax = plt.subplots()

x = len(t_data)
y=t_data[0][0]
yerr_temp = ((t_data[0][0]) - (t_data[0][2]))

ax.bar(x, y, width = 0.2, color='gold', yerr = yerr_temp)
ax.set_title('Temp Min, Max and Avg')

# add some text for labels, title and axes ticks
ax.set_ylabel('Temp(F)')
ax.set_title('Min, Max and Avg Temp of Hawaii')


fig.tight_layout()
plt.show()



# In[456]:

from flask import Flask, jsonify

# Flask Setup
#################################################
app = Flask(__name__)


# In[457]:

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return a list of all passenger names"""
    # Query all passengers
    prcp_query = session.query(func.strftime(measurements.date), (measurements.prcp)).                    filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).all()

    # Convert list of tuples into normal list
    prcp_dates = list(np.ravel(prcp_query))

    return jsonify(prcp_dates)


# @app.route("/api/v1.0/stations")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:



