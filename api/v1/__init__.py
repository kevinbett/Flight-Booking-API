import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask (__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.v1.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

from api.v1.auth.views import auth_blueprint
from api.v1.flight.views import flight_blueprint
from api.v1.images.views import passport_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(flight_blueprint)
app.register_blueprint(passport_blueprint)
