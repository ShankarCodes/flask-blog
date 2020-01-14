from datetime import datetime,timedelta
from .app import db
from .app import login
from .app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt

class User(UserMixin,db.Model):
    __tablename__ = "user"
    
    username = db.Column(db.String(64),index=True,unique=True,primary_key=True)
    email = db.Column(db.String(200),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    last_reset_password_token = db.Column(db.String())
    valid_reset_password_token = db.Column(db.String())
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): 
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} email={self.email} password={self.password_hash}>'
    
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.set_password(password)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()        
        except Exception as e:
            print(e)
            db.session.rollback()
    
    def get_id(self):
        return self.username
    
    def get_password_reset_token(self,expiry):
        payload = {
        'username':self.username,
        'exp':datetime.utcnow()+timedelta(seconds=expiry)
        }
        token =  jwt.encode(payload,app.config['SECRET_KEY'],'HS256')
        token = token.decode('utf-8')
        self.valid_reset_password_token = token
        return token

    def check_password_reset_token(self,token):
        isvalid =  (token != self.last_reset_password_token) and (token == self.valid_reset_password_token) 
        if not isvalid:
            return "NV"
        else:
            return "V"
@login.user_loader
def load_user(username):
    return User.query.get(username)
