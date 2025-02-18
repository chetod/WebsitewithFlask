from flask import Flask, render_template, redirect, url_for, flash,request,session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from forms import RegisterForm,LoginForm
from models import db, User
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundshare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.permanent_session_lifetime = timedelta(days=7)

db.init_app(app)
# Login required decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

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
    
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            flash('เข้าสู่ระบบสำเร็จ', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username หรือ Password ไม่ถูกต้อง', 'danger')
        
        

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ออกจากระบบสำเร็จ', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)