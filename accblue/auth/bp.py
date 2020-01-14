from flask import Blueprint

bp = Blueprint('auth',__name__,url_prefix='/accounts')


from ..app import db
from ..app import login
from ..app import app