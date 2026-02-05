from flask import Flask

from config import Config
from app.extensions import db, migrate
from app.api.routes_api import api_blueprint
from app.web.routes_web import app_blueprint
from app import models
from app.web import errors

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(app_blueprint)
