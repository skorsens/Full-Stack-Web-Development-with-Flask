from flask import Flask
from config import Config
from mongoengine import connect
from flask_restx import Api


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

connect(
    db=app.config["MONGODB_DB"],
    host=app.config["MONGODB_HOST"],
    port=app.config["MONGODB_PORT"],
)

from application import routes
