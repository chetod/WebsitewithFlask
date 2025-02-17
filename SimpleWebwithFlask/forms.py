from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField, IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('ลงทะเบียน')