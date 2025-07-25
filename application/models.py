from mongoengine import Document, IntField, StringField
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document):
    user_id = IntField(unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    email = StringField(max_length=50, unique=True)
    password = StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Course(Document):
    courseID = StringField(max_length=10, unique=True)
    title = StringField(max_length=100)
    description = StringField(max_length=500)
    credits = IntField()
    term = StringField(max_length=25)


class Enrollment(Document):
    user_id = IntField()
    courseID = StringField(max_length=10)
