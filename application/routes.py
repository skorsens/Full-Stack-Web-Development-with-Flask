from application import app


@app.route("/")
@app.route("/index")
def index():
    """Index route"""
    return "<h1>Welcome to the Enrollment Application!</h1>"
