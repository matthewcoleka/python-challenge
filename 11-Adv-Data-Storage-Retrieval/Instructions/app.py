import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

from datetime import datetime
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################
#Creating app
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_dt<br/>"
        f"/api/v1.0/start_dt/end_dt"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    #Creating range for year from last date
    last_dt = (session.query(Measurement.date).order_by(desc(Measurement.date)).first())
    last_dt = datetime.strptime(last_dt[0], '%Y-%m-%d')
    yr_last = last_dt - dt.timedelta(days=365.2422)
    #Querying for results
    query = session.query(Measurement.date, Measurement.prcp, Measurement.tobs). \
    filter(Measurement.date>yr_last).order_by(Measurement.date).all()
    #Putting results in a dictionary
    results = []
    for result in query:
        results_dict ={}
        results_dict['date']=result.date
        results_dict['precipitation']=result.prcp
        results_dict['temp']=result.tobs
        results.append(results_dict)
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    #Creating range for year from last date
    last_dt = (session.query(Measurement.date).order_by(desc(Measurement.date)).first())
    last_dt = datetime.strptime(last_dt[0], '%Y-%m-%d')
    yr_last = last_dt - dt.timedelta(days=365.2422)
    #Query for temperature observations for the previous year
    results = session.query(Measurement.tobs).filter(Measurement.date>yr_last).all()
    all_temps = list(np.ravel(results))
    return jsonify(all_temps)

@app.route("/api/v1.0/<start_dt>")
def start(start_dt):
    try:
        query_start_dt = datetime.strptime(start_dt, '%m-%d-%Y')

        query = session.query((func.min(Measurement.tobs)).label('Temp_Min'), \
            (func.avg(Measurement.tobs)).label('Temp_Avg'), (func.max(Measurement.tobs)).label('Temp_Max')).\
            filter(Measurement.date >= query_start_dt).all()
        #Putting results in a dictionary
        results = []
        for result in query:
            results_dict ={}
            results_dict['TMIN']=result.Temp_Min
            results_dict['TAVG']=result.Temp_Avg
            results_dict['TMAX']=result.Temp_Max
            results.append(results_dict)
        return jsonify(results)
    except ValueError:
        return jsonify({"error": "Enter Date as MM-DD-YYYY"}), 404

@app.route("/api/v1.0/<start_dt>/<end_dt>")
def start_end(start_dt, end_dt):
    try:
        query_start_dt = datetime.strptime(start_dt, '%m-%d-%Y')
        query_end_dt = datetime.strptime(end_dt, '%m-%d-%Y')

        query = session.query((func.min(Measurement.tobs)).label('Temp_Min'), \
            (func.avg(Measurement.tobs)).label('Temp_Avg'), (func.max(Measurement.tobs)).label('Temp_Max')).\
            filter(Measurement.date >= query_start_dt).filter(Measurement.date <= query_end_dt).all()

        #Putting results in a dictionary
        results = []
        for result in query:
            results_dict ={}
            results_dict['TMIN']=result.Temp_Min
            results_dict['TAVG']=result.Temp_Avg
            results_dict['TMAX']=result.Temp_Max
            results.append(results_dict)
        return jsonify(results)
    except ValueError:
        return jsonify({"error": "Enter Date as MM-DD-YYYY"}), 404



if __name__ == '__main__':
    app.run(debug=True)
