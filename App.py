#1. Import Flask and Modules used in Jupyter Notebook 
from flask import Flask, jsonify

import sqlite3
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#2. Database Setup & reflect for tables
engine = create_engine("sqlite:////Users\rober\OneDrive\Desktop\BootCamp HW Folder\My Homework Submission\sqlalchemy-challenge\Resources\hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)

session = Session(engine)
# Create our session (link) from Python to the DB
measurements = Base.classes.measurement
stations = Base.classes.station

#3. Create app, passing __name__
app = Flask(__name__)

#3. Define what to do when a user hits index route
@app.route("/")
def weclome():
    print('Welcome to my "Home" page! Here are the available API Routes for Surfs Up:')
    return (
        f"Available API Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start>:<br/>"
        f"/api/v1.0/<start>/<end>"
    )