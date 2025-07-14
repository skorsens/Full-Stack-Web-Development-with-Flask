import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key_default")

    MONGODB_SETTINGS = {
        "db": "UTA_Enrollment",
    }
