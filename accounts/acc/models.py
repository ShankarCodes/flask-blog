from datetime import datetime,timedelta
from .app import db
from .app import login
from .app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
import hashlib

class User(UserMixin,db.Model):
    __tablename__ = "user"
    
    username = db.Column(db.String(64),index=True,unique=True,primary_key=True,nullable=False)
    email = db.Column(db.String(200),index=True,unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    last_reset_password_token = db.Column(db.String())
    valid_reset_password_token = db.Column(db.String())
    posts = db.relationship('Post', backref='author', lazy=True)
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
    def get_avatar_url(self,size):
        usrhsh = hashlib.md5(bytes(self.username,'utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{usrhsh}?d=identicon&s={size}"
class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True,index = True)
    pub_date = db.Column(db.DateTime,index = True,default = datetime.utcnow )
    
    title = db.Column(db.String(150),nullable = False)
    body = db.Column(db.String,nullable = False)    
    writer = db.Column(db.String,db.ForeignKey('user.username'),nullable=False)
    
    def __repr__(self):
        return f'<Post title={self.title} author={self.writer}'
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()        
        except Exception as e:
            print(e)
            db.session.rollback()
@login.user_loader
def load_user(username):
    return User.query.get(username)
