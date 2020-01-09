from flask import render_template
from flask import Response
from .app import app

@app.route('/')
@app.route('/index')
def home_page():
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
 
    return render_template('index.html',user=sampleuser,posts=posts)