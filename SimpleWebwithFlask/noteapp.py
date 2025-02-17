from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from forms import RegisterForm
from models import db, User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundshare.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=username).first():
                flash('Username นี้ถูกใช้งานแล้ว', 'danger')
                return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
                flash('Email นี้ถูกใช้งานแล้ว', 'danger')
                return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
            
        flash('ลงทะเบียนสำเร็จ กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)