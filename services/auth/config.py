import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # APP
    FLASK_ENV = os.environ.get("FLASK_ENV", None)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", None)
    FLASK_APP = os.environ.get("FLASK_APP", None)
    FLASK_PORT = os.environ.get("FLASK_AUTH_PORT", None)
    FLASK_TESTING = os.environ.get("FLASK_TESTING", None)
    SECRET_KEY = os.urandom(24)
    SERVICE_MAILER = os.environ.get("SERVICE_MAILER", None)
    SERVICE_WEB = os.environ.get("SERVICE_WEB", None)
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
