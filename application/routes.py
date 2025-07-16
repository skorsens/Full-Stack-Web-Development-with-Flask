import json

from application import app
from flask import render_template, request, Response, flash, redirect

from application.forms import LoginForm, RegisterForm
from application.models import Enrollment, User, Course


lCoursesData = [
    {
        "courseID": "1111",
        "title": "PHP 101",
        "description": "Intro to PHP",
        "credits": 3,
        "term": "Fall, Spring",
    },
    {
        "courseID": "2222",
        "title": "Java 1",
        "description": "Intro to Java Programming",
        "credits": 4,
        "term": "Spring",
    },
    {
        "courseID": "3333",
        "title": "Adv PHP 201",
        "description": "Advanced PHP Programming",
        "credits": 3,
        "term": "Fall",
    },
    {
        "courseID": "4444",
        "title": "Angular 1",
        "description": "Intro to Angular",
        "credits": 3,
        "term": "Fall, Spring",
    },
    {
        "courseID": "5555",
        "title": "Java 2",
        "description": "Advanced Java Programming",
        "credits": 4,
        "term": "Fall",
    },
]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if request.form.get("email") == "test@uta.com":
            flash("You have successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Something went wrong. Please try again.", "danger")

    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template(
        "courses.html", lCoursesData=lCoursesData, courses=True, term=term
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if request.form.get("email") == "test@uta.com":
            flash("You have successfully registered!", "success")
            return redirect("/index")
        else:
            flash("Something went wrong. Please try again.", "danger")

    return render_template(
        "register.html", title="New User Registration", form=form, register=True
    )


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    courseID = request.form.get("courseID")
    title = request.form.get("title")
    term = request.form.get("term")
    return render_template(
        "enrollment.html",
        enrollment=True,
        data={"courseID": courseID, "title": title, "term": term},
    )


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx: str = None):
    status = 200

    if idx is None:
        jdata = lCoursesData
    else:
        try:
            nIdx = int(idx)
            jdata = lCoursesData[nIdx]
        except (ValueError, IndexError):
            jdata = {"error": f"Course id {idx} not found"}
            status = 404

    return Response(json.dumps(jdata), mimetype="application/json", status=status)


@app.route("/user")
def user():
    # User(
    #     user_id=1,
    #     first_name="FN_1",
    #     last_name="LN_1",
    #     email="email_1@email.com",
    #     password="12345",
    # ).save()
    # User(
    #     user_id=2,
    #     first_name="FN_2",
    #     last_name="LN_2",
    #     email="email_2@email.com",
    #     password="67890",
    # ).save()

    users = User.objects.all()
    return render_template("user.html", users=users)
