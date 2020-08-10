import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_ENV = os.environ.get("FLASK_ENV", None)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", None)
    FLASK_APP = os.environ.get("FLASK_APP", None)
    FLASK_PORT = os.environ.get("SCHEDULER_FLASK_PORT", None)
    FLASK_TESTING = os.environ.get("FLASK_TESTING", 0)
    INGRESS = os.environ.get("INGRESS", None)
    SECRET_KEY = os.urandom(24)
