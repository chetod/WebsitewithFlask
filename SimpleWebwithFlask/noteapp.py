from flask import Flask, render_template, redirect, url_for, flash,request,session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from forms import RegisterForm,LoginForm,SoundPostForm,CommentForm,RatingForm
from models import db, User,Category,SoundPost,Comment,Rating
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundshare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.permanent_session_lifetime = timedelta(days=7)

db.init_app(app)

# สร้างโฟลเดอร์สำหรับเก็บไฟล์เสียง
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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
    # แสดงเสียงยอดนิยม
    top_played = SoundPost.query.order_by(SoundPost.play_count.desc()).limit(5).all()
    # แสดงเสียงที่มีคะแนนสูงสุด
    top_rated = SoundPost.query.all()
    top_rated = sorted(top_rated, key=lambda x: x.average_rating, reverse=True)[:5]
    # แสดงเสียงล่าสุด
    latest = SoundPost.query.order_by(SoundPost.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         top_played=top_played,
                         top_rated=top_rated,
                         latest=latest)

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

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', username=user.username)    

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = SoundPostForm()
    categories = Category.query.all()
    if not categories:
        default_categories = ["Music", "Podcast", "Nature Sounds", "Instrumental", "ASMR"]
        for name in default_categories:
            db.session.add(Category(name=name))
        db.session.commit()
        categories = Category.query.all()  # reload categories after adding default ones
    form.category.choices = [(c.id, c.name) for c in categories]
    if form.validate_on_submit():#check when press button summit
        file = form.sound_file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # create path to save file
        file.save(file_path)
        
        post = SoundPost( # create new post
            title=form.title.data,
            description=form.description.data,
            file_path=filename,
            user_id=session['user_id'],
            category_id=form.category.data
        )
        db.session.add(post) # add post to database
        db.session.commit() # commit changes
        
        flash('Your sound has been posted!', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = SoundPost.query.get_or_404(post_id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    if request.method == 'POST' and 'user_id' in session: # check if user is logged in and there is a POST request
        # Check if this is a comment submission
        if comment_form.validate_on_submit():
            comment = Comment(
                content=comment_form.content.data,
                user_id=session['user_id'],
                post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('post', post_id=post_id))
        
        # Check if this is a rating submission
        if rating_form.validate_on_submit():
            existing_rating = Rating.query.filter_by( #chheck if user already rated this post
                user_id=session['user_id'],
                post_id=post_id
            ).first()

            if existing_rating: 
                existing_rating.value = rating_form.value.data
            else:
                rating = Rating(
                    value=rating_form.value.data,
                    user_id=session['user_id'],
                    post_id=post_id
                )
                db.session.add(rating)
            db.session.commit()
            flash('Rating added!', 'success')
            return redirect(url_for('post', post_id=post_id))

    return render_template('post.html', 
                         post=post,
                         comment_form=comment_form,
                         rating_form=rating_form)

     
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)