from flask import Flask

app = Flask(__name__)

from app import route
from app.uploader import uploader_blueprint
from app.validate import validate_blueprint
from app.configure import configure_blueprint


app.register_blueprint(uploader_blueprint)
app.register_blueprint(validate_blueprint)
app.register_blueprint(configure_blueprint)