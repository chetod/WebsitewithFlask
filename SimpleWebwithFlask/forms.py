from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField, IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120), Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('ลงทะเบียน')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('เข้าสู่ระบบ')

class SoundPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    sound_file = FileField('Sound File', validators=[
        FileAllowed(['mp3', 'wav'], 'Audio files only!')
    ])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])

class RatingForm(FlaskForm):
    value = IntegerField('Rating', validators=[
        DataRequired(),
        NumberRange(min=1, max=5)
    ])

class ProfileForm(FlaskForm):
    about = TextAreaField('About', validators=[Length(max=500)])
    profile_image = FileField('Profile Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')
