from flask import render_template
from flask import Response
from flask import redirect
from flask import flash,url_for
from flask import request
from .app import app
from .forms import LoginForm,RegisterForm,ResetPasswordForm,ForgotPasswordForm
from .models import User
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
@app.route('/')
@app.route('/index')
def home_page():
    return render_template('home_page.html')
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)#.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home_page'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        u2 = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash('Username already exists')
            return redirect(url_for('register'))
        if u2 is not None:
            flash('Email already exists')
            return redirect(url_for('register'))
        else:
            usr = form.username.data
            password = form.password.data
            email = form.email.data
            u = User(username=usr,email=email,password=password)
            u.save()
            login_user(u, remember=False)
        return redirect(url_for('home_page'))
    return render_template('register.html',form=form)


@app.route('/forgotpassword',methods=['POST','GET'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        usr = User.query.get(form.username.data)
        if usr is not  None:
            token = usr.get_password_reset_token(60)
            print(f"{request.base_url}/passwordreset?token={token.decode('utf-8')}")
        return render_template('mail_sent_forgot_password.html')
    return render_template('forgot_password.html',form=form)

@app.route('/forgotpassword/passwordreset')
def reset_password():
    form = ResetPasswordForm()
    token = request.args.get("")
    return render_template('reset_password.html',form=form)
"""
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
    
 
    return render_template('index.html',posts=posts)




"""