from flask_wtf import FlaskForm#, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ContactForm(FlaskForm):
    name = StringField('Name',[DataRequired()])
    email = StringField('Email',[Email(message="Not a valid Email"),
                                 DataRequired(),
                                 ])
    body = TextField('message',[DataRequired(),
                                Length(min=10,message="Your message is too small"),
                                Length(max=200,message="Your message is too long"),
                                ])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Sumbit')
    