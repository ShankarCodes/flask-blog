from flask import render_template
from flask import Response
from flask import redirect,abort
from flask import flash,url_for
from flask import request
from .app import app
from .forms import LoginForm,RegisterForm,ResetPasswordForm,ForgotPasswordForm
from .models import User,Post
from .mail import sendmail
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required
import jwt
from jinja2 import Template

tpl = Template('''<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        crossorigin="anonymous"></script>
<h1>Hi {{username}}</h1>
<p>We have recieved a request to change the password for your account</p>
<p>If you had requested for a password reset,please click 
<a class="btn btn-primary" href={{reset_url}}>Reset Password</a></p>
<p>Or copy and paste this link {{reset_url}} in your browser</p>
<p><strong>Note:This url will only be valid for 3 hours</strong></p>
<p>If you had not requested for a password change,you can safely ignore this email</p>
            ''')


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
    print(form.errors)
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
            token = usr.get_password_reset_token(2*60*60)
            usr.save()
            url = f"{request.base_url}/passwordreset?token={token}"
            resp = tpl.render(username=usr.username,reset_url=url)
            
            sendmail('ShankarSupport@shankar-login.herokuapp.com',usr.email,'Request for password reset for your account',resp)
        return render_template('mail_sent_forgot_password.html')
    return render_template('forgot_password.html',form=form)

@app.route('/forgotpassword/passwordreset',methods=['GET','POST'])
def reset_password():
    form = ResetPasswordForm()
    token = request.args.get("token")
    if token is None :
        return render_template('invalid_reset_password.html',msg="No Token")
    else:
        try:
            decoded = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return render_template('invalid_reset_password.html',msg="Invalid Token")
        usr = User.query.get(decoded['username'])
        print(usr)
        su = usr.check_password_reset_token(token)
        usr.save()
        if su == 'NV':
            return render_template('invalid_reset_password.html',msg="Invalid Token")
        else:
            if form.validate_on_submit():
                usr.set_password(form.password.data)
                usr.last_reset_password_token = token
                usr.save()
                return "SUCESS"
    
    return render_template('reset_password.html',form=form)

@app.route('/user/<username>')
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user_page.html',user=user,posts=posts)

@app.route('/user/')
def user():
    if current_user.is_authenticated:
        return redirect(url_for('user_page',username=current_user.username))
    else:
        return redirect(url_for('login'))

@app.route('/post/<int:id>')
def post_page(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    else:
        return render_template('post_view.html',post=post)

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