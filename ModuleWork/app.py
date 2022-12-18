from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''') 

#@app.route('/api/v1.0/precipitation')
#def find_station():
#    testing = []
#    testing1 = session.query(Measurement.station).distinct().all()
#    testing = [x[0] for x in testing1]
#    return jsonify(testing)

@app.route('/api/v1.0/precipitation')
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date2 = dt.datetime.strptime(last_date, '%Y-%m-%d')
    actual_date = last_date2.date()
    #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prev_year = actual_date - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    #stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    results =  session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route('/api/v1.0/tobs')
def temp_monthly():
    #tobss = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()
    #return jsonify(tobss)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#@app.route('/api/v1.0/temp/start/end')
#def temp_monthly():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#    results = session.query(Measurement.tobs).\
#        filter(Measurement.station == 'USC00519281').\
#            filter(Measurement.date >= prev_year).all()
#    temps = list(np.ravel(results))
#    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None,end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#if __name__ == "__main__":
#    app.run(debug=True)