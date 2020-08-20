# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    """Home Page: Here are the Available API Routes for Surfs Up"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_date = (dt.datetime.strptime(latest_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    query_cols = (measurement.date, measurement.prcp)
    year_data = session.query(*query_cols).filter(measurement.date >= one_year_date).all()
    
    precip_dict = []
    for result in year_data:
        r = {}
        r[result[0]] = result[1]
        precip_dict.append(r)
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station, station.name).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def observations():
    session = Session(engine)
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_date = (dt.datetime.strptime(latest_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    year_data = session.query(measurement.date, measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date > one_year_date).all()
    return jsonify(year_data)

@app.route("/api/v1.0/temp/start")
def start_dt(start_dt):
    session = Session(engine)
    start = dt.datetime.strptime(start_dt, '%Y-%m-%d')
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= start).all()
    start_list = []
    for c in results:
        c = {}
        c["Start Dt"] = start
        c["Temp_Min"] = results[0]
        c["Temp Max"] = results[1]
        c["Temp Avg"] = results[2]
        start_list.append(c)
    return jsonify(start_list)

@app.route("/api/v1.0/temp/start/end")
def start_end(start_dt,end_dt):
        session = Session(engine)
        start = dt.datetime.strptime(start_dt, '%Y-%m-%d')
        end = dt.datetime.strptime(end_dt, '%Y-%m-%d')
        results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= start).\
                filter(measurement.date <= end).all()
        result_list = []
        for c in results:
            c = {}
            c["Start Dt"] = start
            c["End Dt"] = end
            c["Temp_Min"] = results[0]
            c["Temp Max"] = results[1]
            c["Temp Avg"] = results[2]
            result_list.append(c)
        return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)