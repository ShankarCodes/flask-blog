from flask import render_template
from flask import Response
from .app import app
from .forms import LoginForm

sampleuser = {'username':'Shankar'}
posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

@app.route('/')
@app.route('/index')
def home_page():
    
 
    return render_template('index.html',user=sampleuser,posts=posts)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',form=form,user=sampleuser)