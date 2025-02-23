from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField, IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class RegisterForm(FlaskForm):# สร้างฟอร์มลงทะเบียน
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120), Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('ลงทะเบียน')

class LoginForm(FlaskForm):# สร้างฟอร์มเข้าสู่ระบบ
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('เข้าสู่ระบบ')

class SoundPostForm(FlaskForm):# สร้างฟอร์มโพสต์เสียง
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    sound_file = FileField('Sound File', validators=[ # สร้างฟิลด์เสียง
        FileAllowed(['mp3', 'wav'], 'Audio files only!') # กำหนดนามสกุลไฟล์เสียง
    ])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):# สร้างฟอร์มคอมเม้นต์
    content = TextAreaField('Comment', validators=[DataRequired()])

class RatingForm(FlaskForm):
    value = IntegerField('Rating', validators=[
        DataRequired(),
        NumberRange(min=1, max=5)
    ])

class ProfileForm(FlaskForm):# สร้างฟอร์มโปรไฟล์
    about = TextAreaField('About', validators=[Length(max=500)])
    profile_image = FileField('Profile Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')
