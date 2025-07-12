from flask import Flask


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    """Index route"""
    return "<h1>Welcome to the Enrollment Application!</h1>"
