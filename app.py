from flask import Flask
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Configure the Flask application
config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(config_type)

#Remove the default logger configured by Flask
app.logger.removeHandler(default_handler)

#Logging Configuration
file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')

# Import blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

# Register blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')
