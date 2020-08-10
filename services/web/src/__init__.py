import logging
import os
from flask_ckeditor import CKEditor
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()


def create_app(test_config=False):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False, static_url_path='/static')
    if not test_config:
        logging.info(":::__init__.py::: DEV")
        app.config.from_object('config.Config')
    else:
        logging.info(":::__init__.py::: TESTUJEMY")
        app.config.from_object('config.TestConfig')
        app.config.update(
            BCRYPT_LOG_ROUNDS=4,
            HASH_ROUNDS=1,
            LOGIN_DISABLED=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY=os.urandom(25),
            TESTING=True
        )

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    logging.info(':::__init__.py::: Starting app')
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    with app.app_context():
        # Include our Routes
        from flask_bootstrap import Bootstrap
        from . import routes
        from . import auth

        # Register Blueprints
        # app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        logging.info(':::__init__.py::: Creating database')
        Bootstrap(app)
        db.create_all()
        logging.info(':::__init__.py::: Database created')

        return app, logging