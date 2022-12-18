from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/station')
def find_station():
    testing = []
    testing1 = session.query(Measurement.station).distinct().all()
    testing = [x[0] for x in testing1]
    return jsonify(testing)

if __name__ == "__main__":
    app.run(debug=True)


#using the above code means we can run the app locally without worry
#if we wanted to run from the terminal we could use 
#export FLASK_APP=app.py
#then
#flask run

#Below is what you might run if we were needing to call the functions/routes from this code
#import app

#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#    print("example is being run directly.")
#else:
#    print("example is being imported")
