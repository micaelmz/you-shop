from flask import Flask
from view import view_blueprint
from api import api_blueprint
from utils.database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

app.register_blueprint(view_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')
