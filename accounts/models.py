from datetime import datetime
from .app import db
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(200),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}, email={self.email}>'
