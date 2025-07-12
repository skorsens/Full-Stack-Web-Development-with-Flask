from application import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    """Index route"""
    return render_template("index.html")
