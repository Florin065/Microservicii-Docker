from flask import Flask
from .db import initialize_db
from .routes import api


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/weather_db"

    initialize_db(app)

    app.register_blueprint(api)

    return app
