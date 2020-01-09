from .config import Config
# A Basic Flask App
from flask import Flask
app = Flask(__name__)
app.config.from_object(Config)