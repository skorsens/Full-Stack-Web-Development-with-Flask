from flask import Flask
from config import Config
from mongoengine import connect

app = Flask(__name__)
app.config.from_object(Config)

connect(
    db=app.config['MONGODB_DB'],
    host=app.config['MONGODB_HOST'],
    port=app.config['MONGODB_PORT'],
)

from application import routes
