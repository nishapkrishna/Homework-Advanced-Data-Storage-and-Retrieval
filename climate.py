# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime 
from flask import Flask, jsonify
#from sqlalchemy.orm import scoped_session, sessionmaker
# 1. import Flask
from flask import Flask

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

# Design a query to retrieve the last 12 months of precipitation data and plot the results
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Get the first element of the tuple
    max_date = max_date[0]

# one_year_ago calculation
    one_year_ago = datetime.datetime.strptime(max_date, "%Y-%m-%d") - datetime.timedelta(days=366)

    prcp = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > one_year_ago).\
    order_by(Measurement.date).all()

# Create a dictionary from the row data and append to a list
    all_prcp= []
    for eachRow in prcp:
        prcp_dict = {}
        prcp_dict["date"] =eachRow.date
        prcp_dict["prcp"] =eachRow.prcp
        all_prcp.append(prcp_dict)
        session.close()
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    """List all Stations"""
    Stations = session.query(Station.id, Station.name).all()

# Create a dictionary from the row data and append to a list
    all_stn= []
    for eachRow in Stations:
        stn_dict = {}
        stn_dict["id"] =eachRow.id
        stn_dict["name"] =eachRow.name
        all_stn.append(stn_dict)
        session.close()
    return jsonify(all_stn)

@app.route("/api/v1.0/tobs")
def tobs():

# Design a query to retrieve the last 12 months of precipitation data and plot the results
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Get the first element of the tuple
    max_date = max_date[0]

# one_year_ago calculation
    one_year_ago = datetime.datetime.strptime(max_date, "%Y-%m-%d") - datetime.timedelta(days=366)

    """List all Tobs"""

    tobs_val = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > one_year_ago).\
    order_by(Measurement.date).all()    

# Create a dictionary from the row data and append to a list
    all_tobs = []
    for eachRow in tobs_val:
        tobs_dict = {}
        tobs_dict["date"] = eachRow.date
        tobs_dict["tobs"] = eachRow.tobs
        all_tobs.append(tobs_dict)
        session.close()
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def tempCalcStart(start_date):  

# Set the start and end date of the trip
#    start_date = '2017-02-28'

# Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    tempList=  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

# Create a dictionary from the row data and append to a list
    all_tempCals= []
    t_dict = {}
    t_dict["min"] =tempList[0][0]
    t_dict["avg"] =tempList[0][1]
    t_dict["max"] =tempList[0][2]
    all_tempCals.append(t_dict)
    session.close()
    return jsonify(all_tempCals)    

@app.route("/api/v1.0/<start_date>/<end_date>")
def tempCalc(start_date,end_date):

# Set the start and end date of the trip
#    start_date = '2017-02-28'
#    end_date = '2017-03-08'

# Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    tempList= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
# Create a dictionary from the row data and append to a list
    all_tempCals= []
    t_dict = {}
    t_dict["min"] =tempList[0][0]
    t_dict["avg"] =tempList[0][1]
    t_dict["max"] =tempList[0][2]
    all_tempCals.append(t_dict)
    session.close()
    return jsonify(all_tempCals)

if __name__ == "__main__":
   app.run(debug=True)







