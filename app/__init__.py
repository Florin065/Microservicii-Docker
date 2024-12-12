from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/weather_db"
mongo = PyMongo(app)

db = mongo.db
db.countries.create_index('nume', unique=True)
db.cities.create_index('idTara', unique=True)
db.cities.create_index('nume', unique=True)
db.temperatures.create_index('idOras', unique=True)
db.temperatures.create_index('timestamp', unique=True)

from app import routes
