from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from config import config

# Create unitialized extentions
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

def create_app(config_name):
    # Create and Configure App
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Extentions
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

