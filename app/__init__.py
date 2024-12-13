from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/weather_db"
mongo = PyMongo(app)

db = mongo.db
db.countries.create_index('nume', unique=True)
db.cities.create_index([('nume', 1), ('idTara', 1)], unique=True)
db.temperatures.create_index([('idOras', 1), ('timestamp', 1)], unique=True)

from app import routes
