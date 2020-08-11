from flask import Flask


def create_app(test_config=None):
    app = Flask('ml_service')
    if test_config:
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.BaseConfig', )

    with app.app_context():
        from src import routes

    return app