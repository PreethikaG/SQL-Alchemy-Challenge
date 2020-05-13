import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start/</br>"
        f"/api/v1.0/start/end/"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    precip = []

    for date,prcp in results:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = prcp
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    results = session.query(func.distinct(Measurement.station)).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#/api/v1.0/tobs`
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    last_data_point = session.query(func.max(Measurement.date)).first()
    active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == active_station[0][0]).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23' )
    session.close()

    temp = []


    for date,tobs in results:
        temp_dict = {}
        temp_dict['Date'] = date
        temp_dict['Temperature'] = tobs
        temp.append(temp_dict)
    return jsonify(temp)


#`/api/v1.0/<start>`  
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
# for a given start or start-end range.When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater 
# than and equal to the start date.

@app.route("/api/v1.0/<start>/")
def start_date(start):
    session =Session(engine)
    #str_date = start.strftime("%Y-%m-%d")
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    return jsonify(results)

#`/api/v1.0/<start>/<end>` When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
# for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>/")
def startdate_enddate(start,end):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
