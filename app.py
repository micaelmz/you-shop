from flask import Flask
from view import view_blueprint
from api import api_blueprint

app = Flask(__name__)

app.register_blueprint(view_blueprint)
app.register_blueprint(api_blueprint)
