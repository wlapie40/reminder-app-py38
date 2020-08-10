from src import create_app

app, logging = create_app()

logging.info(':::wsgi.py::: SCHEDULER INITIALIZING')
logging.info(f':::wsgi.py::: SCHEDULER_FLASK_PORT: {app.config.get("FLASK_PORT")}')

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=app.config.get("FLASK_PORT"),
            debug=app.config.get("FLASK_DEBUG"))
