from src import create_app

app, logging = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=app.config.get("FLASK_PORT"),
            debug=app.config.get("FLASK_DEBUG"))