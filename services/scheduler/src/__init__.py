import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask

from .job import cron_job_notes_recall

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Globally accessible libraries

sched = BlockingScheduler()


def create_app(test_config=False):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
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

    logging.info(':::__init__.py::: core-scheduler Starting app')
    with app.app_context():
        logging.info(':::__init__.py::: core-scheduler adding cron_job')
        sched.add_job(job.cron_job_notes_recall, 'cron', hour=5, minute=00)
        # sched.add_job(job.cron_job_notes_recall, 'interval', seconds=3)
        sched.start()
        logging.info(':::__init__.py::: core-scheduler job started')

        return app, logging