import json

from application import app
from flask import render_template, request, Response, flash, redirect, url_for

from application.forms import LoginForm, RegisterForm
from application.models import Enrollment, User, Course


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # request.form.get("email") == form.email.data
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if not user:
            flash(f"The email not found: {email}. Please try again.", "danger")
        elif user.check_password(password):
            flash(f"{user.first_name}: You have successfully registered!", "success")
            return redirect("/index")
        else:
            flash(f"Wrong password {password}. Please try again.", "danger")

    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    lCoursesData = Course.objects.order_by("-courseID")

    return render_template(
        "courses.html", lCoursesData=lCoursesData, courses=True, term=term
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # request.form.get("email") == form.email.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user_id = User.objects.count() + 1

        user = User(
            user_id=user_id, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()

        flash(f"{user.first_name}: You have successfully registered!", "success")
        return redirect(url_for("index"))

    return render_template(
        "register.html", title="New User Registration", form=form, register=True
    )


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = 1

    mongoDbPipeline = [
        {
            "$lookup": {
                "from": "enrollment",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "r1",
            }
        },
        {
            "$unwind": {
                "path": "$r1",
                "includeArrayIndex": "r1_id",
                "preserveNullAndEmptyArrays": False,
            }
        },
        {
            "$lookup": {
                "from": "course",
                "localField": "r1.courseID",
                "foreignField": "courseID",
                "as": "r2",
            }
        },
        {"$unwind": {"path": "$r2", "preserveNullAndEmptyArrays": False}},
        {"$match": { "user_id": user_id }},
        {"$sort": { "courseID": 1 }},
    ]
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(
                f"You are already enrolled in the course: {courseTitle} ({courseID})",
                "warning",
            )
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(
                f"You have successfully enrolled in the course: {courseTitle} ({courseID})",
                "success",
            )

        lCoursesData = list(User.objects.aggregate(*mongoDbPipeline))
    else:
        lCoursesData = []

    return render_template(
        "enrollment.html",
        enrollment=True,
        title="Enrollment",
        lCoursesData=lCoursesData,
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
