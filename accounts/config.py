import os
basedir = os.path.abspath(os.path.dirname(__file__))

#os.environ['DATABASE_URI']='postgresql+psycopg2://shankar2:shankarsr123@localhost/learn'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key-keep-it-safe'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
