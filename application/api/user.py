from flask_restx import Namespace, Resource, fields

from application.models import User


user_namespace = Namespace("user", description="User related operations")


dPostUserModel = user_namespace.model(
    "UserPost",
    {
        "email": fields.String(required=True, description="User email"),
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "password": fields.String(required=True, description="Password"),
    },
)

dPutUserModel = user_namespace.model(
    "UserPut",
    {
        "email": fields.String(required=False, description="User email"),
        "first_name": fields.String(required=False, description="First name"),
        "last_name": fields.String(required=False, description="Last name"),
        "password": fields.String(required=False, description="Password"),
    },
)


@user_namespace.route("/api", "/api/")
class CGetAndPostUsers(Resource):
    def get(self):
        Users = User.objects.all()
        return Users.to_json()

    @user_namespace.expect(dPostUserModel)
    def post(self):
        payload = user_namespace.payload
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


@user_namespace.route("/api/<int:idx>")
class CGetUpdateDeleteUser(Resource):
    def get(self, idx: int):
        UserIdx = User.objects(user_id=idx).first()

        if not UserIdx:
            return f"User {idx} does not exist", 404

        return UserIdx.to_json()

    @user_namespace.expect(dPutUserModel)
    def put(self, idx: int):
        UserData = user_namespace.payload
        User.objects(user_id=idx).update(**UserData)
        return User.objects(user_id=idx).to_json()

    def delete(self, idx: int):
        User.objects(user_id=idx).delete()

        return f"User {idx} has been deleted", 200
