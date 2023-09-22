from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
from flask_wtf.file import FileField
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Try another username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Try another email')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Profile Pic')
    age = StringField('Age')
    submit = SubmitField('Готово')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    author = StringField('Author')
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Готово')

