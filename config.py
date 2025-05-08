import os

# from flask_mysqldb import MySQL


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL", "mysql+mysqlconnector://root:password@localhost/py_db_test"
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
