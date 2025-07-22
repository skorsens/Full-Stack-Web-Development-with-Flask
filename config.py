import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", b"\xb2\xf9\x8b\xe9q\xb4M\xad\x80Z?\xedll02"
    )

    MONGODB_SETTINGS = {
        "db": "UTA_Enrollment",
    }
