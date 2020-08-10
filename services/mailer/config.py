import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # APP
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", None)
    EMAIL = os.environ.get("EMAIL", None)
    FLASK_ENV = os.environ.get("FLASK_ENV", None)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", None)
    FLASK_APP = os.environ.get("FLASK_APP", None)
    FLASK_PORT = os.environ.get("FLASK_MAILER_PORT", None)
    FLASK_TESTING = os.environ.get("FLASK_TESTING", None)
    INGRESS = os.environ.get("INGRESS", None)
    SECRET_KEY = os.urandom(24)
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
