import json

from application import app, api
from flask import (
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    session,
)
from flask_restx import Resource, fields

from application.forms import LoginForm, RegisterForm
from application.models import Enrollment, User, Course


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_name"):
        flash(f"Welcome back, {session['user_name']}!", "success")
        return redirect(url_for("index"))

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
            session["user_id"] = user.user_id
            session["user_name"] = user.first_name
            return redirect("/index")
        else:
            flash(f"Wrong password {password}. Please try again.", "danger")

    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session.pop("user_name")

    return redirect(url_for("index"))


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    lCoursesData = Course.objects.order_by("-courseID")

    return render_template(
        "courses.html", lCoursesData=lCoursesData, courses=True, term=term
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_name"):
        flash(f"Welcome back, {session['user_name']}!", "success")
        return redirect("/index")

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
    if not session.get("user_name"):
        flash(f"Please login.", "success")
        return redirect(url_for("login"))

    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = session.get("user_id")

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
        {"$match": {"user_id": user_id}},
        {"$sort": {"courseID": 1}},
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


dPostUserModel = api.model(
    "User",
    {
        "email": fields.String(required=True, description="User email"),
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "password": fields.String(required=True, description="Password"),
    },
)

dPutUserModel = api.model(
    "User",
    {
        "email": fields.String(required=False, description="User email"),
        "first_name": fields.String(required=False, description="First name"),
        "last_name": fields.String(required=False, description="Last name"),
        "password": fields.String(required=False, description="Password"),
    },
)


@api.route("/api", "/api/")
class CGetAndPostUsers(Resource):
    def get(self):
        Users = User.objects.all()
        return Users.to_json()

    @api.expect(dPostUserModel)
    def post(self):
        payload = api.payload
        user_id = User.objects.count() + 1
        email = payload["email"]
        first_name = payload["first_name"]
        last_name = payload["last_name"]
        password = payload["password"]

        user = User(
            user_id=user_id, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()

        return User.objects(user_id=user_id).first().to_json()


@api.route("/api/<int:idx>")
class CGetUpdateDeleteUser(Resource):
    def get(self, idx: int):
        UserIdx = User.objects(user_id=idx).first()

        if not UserIdx:
            return f"User {idx} does not exist", 404

        return UserIdx.to_json()

    @api.expect(dPutUserModel)
    def put(self, idx: int):
        UserData = api.payload
        User.objects(user_id=idx).update(**UserData)
        return User.objects(user_id=idx).to_json()

    def delete(self, idx: int):
        User.objects(user_id=idx).delete()

        return f"User {idx} has been deleted", 200
