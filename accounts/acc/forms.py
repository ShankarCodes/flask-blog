from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired(),Email(message="Not a valid Email")])
    password = PasswordField('Password',validators=[DataRequired()])
    register = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('cpassword', message='Passwords must match')])
    cpassword = PasswordField('Confirm Password',validators=[DataRequired()])
    reset = SubmitField('Reset')

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    ok = SubmitField('OK')