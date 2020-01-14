from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager
from auth import bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)

app.register_blueprint(bp.bp)
#from .models import User
#migrate = Migrate(app,db)
