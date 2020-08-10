import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # APP
    FLASK_ENV = os.environ.get("FLASK_ENV", None)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", None)
    FLASK_APP = os.environ.get("FLASK_APP", None)
    FLASK_PORT = os.environ.get("FLASK_WEB_PORT", None)
    FLASK_TESTING = os.environ.get("FLASK_TESTING", 0)
    FLASK_AUTH_PORT = os.environ.get("FLASK_AUTH_PORT", None)
    INGRESS = os.environ.get("INGRESS", None)
    SECRET_KEY = os.urandom(24)
    SERVICE_AUTH = os.environ.get("SERVICE_AUTH", None)
    SERVICE_MAILER = os.environ.get("SERVICE_MAILER", None)
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
