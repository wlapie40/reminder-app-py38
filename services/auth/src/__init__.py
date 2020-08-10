import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

db = SQLAlchemy()


def create_app(test_config: bool = False):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    if not test_config:
        logging.info("auth ::: create_app ::: PROD")
        app.config.from_object('config.Config')
    else:
        logging.info("auth ::: create_app ::: TESTING")
        app.config.from_object('config.TestConfig')
        app.config.update(
            SECRET_KEY=os.urandom(25),
            TESTING=True
        )
    db.init_app(app)

    logging.info('auth :::__init__.py::: ryanote-auth starting')
    with app.app_context():
        from . import routes

        return app, logging
