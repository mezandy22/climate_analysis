#################################################
# Database Setup
#################################################
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

#import dateime dependicies
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from flask import Flask, jsonify

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the stations class to a variable called `stations`
stations = Base.classes.stations

# Assign the measurements class to a variable called `measurements`
measurements = Base.classes.measurements

# To persist hawaii.sqlite database, we use a Session object
# A session is akin to a conversation between Python and SQL
# Define session
session = Session(bind=engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
last_date = dt.date(2017, 8, 23) 

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp_fun():
    
    # query date and prcp
    prcp_query = session.query(func.strftime(measurements.date), (measurements.prcp)).\
                    filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).all()

    # Convert list of tuples into normal list
    prcp_dates = list(np.ravel(prcp_query))

    return jsonify(prcp_dates)


@app.route("/api/v1.0/stations")
def station_names():
    # Query all passengers
    stations_result = session.query(stations.station).all()

    # convert to list
    stations_list = list(np.ravel(stations_result))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all passengers
    count_stn_obs_yr = session.query(measurements.station, func.count(measurements.station)).\
                filter(measurements.date <= last_date, measurements.date>= last_date-relativedelta(months=12)).\
                group_by(measurements.station).order_by(measurements.tobs).all()

    # convert to list
    stations_obs = list(np.ravel(count_stn_obs_yr))

    return jsonify(stations_obs)

@app.route("/api/v1.0/start")
def calc_temps_start(start_date, end_date='2017-8-23'):
    
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")

    temp_data = session.query(func.max(measurements.tobs), func.avg(measurements.tobs), func.min(measurements.tobs)).\
                filter(measurements.date <= end_date1, measurements.date>= start_date1).all()
    temp_data_list = list(np.ravel(temp_data))

    # t_data = calc_temps('2017-04-18', '2017-04-25')

    return jsonify(temp_data_list)

@app.route("/api/v1.0/end")
def calc_temps_end(end_date, start_date='2017-1-01'):
    
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")

    temp_data = session.query(func.max(measurements.tobs), func.avg(measurements.tobs), func.min(measurements.tobs)).\
                filter(measurements.date <= end_date1).all()
    temp_data_list = list(np.ravel(temp_data))

    # t_data = calc_temps('2017-04-18', '2017-04-25')

    return jsonify(temp_data_list)


    
if __name__ == '__main__':
    app.run(debug=True)
