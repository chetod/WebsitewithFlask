from flask import Flask, render_template, redirect, url_for, flash,request,session,send_from_directory,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import timedelta,datetime
from forms import RegisterForm,LoginForm,SoundPostForm,CommentForm,RatingForm,ProfileForm
from models import db, User,Category,SoundPost,Comment,Rating
from flask_migrate import Migrate
app = Flask(__name__)# สร้าง object ของ Flask
app.config['SECRET_KEY'] = os.urandom(24) # กำหนดค่า SECRET_KEY สำหรับการเข้ารหัส session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundshare.db' # กำหนดที่อยู่ของ database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # ปิดการแจ้งเตือนการเปลี่ยนแปลง
app.config['UPLOAD_FOLDER'] = 'static/uploads'# โฟลเดอร์สำหรับเก็บไฟล์เสียง
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.permanent_session_lifetime = timedelta(days=7) # ให้ session อยู่ 7 วัน
migrate = Migrate(app, db)# สร้าง object สำหรับ migration
db.init_app(app)# สร้าง database

# สร้างโฟลเดอร์สำหรับเก็บไฟล์เสียง
if not os.path.exists(app.config['UPLOAD_FOLDER']): # ถ้ายังไม่มีโฟลเดอร์
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Login required decorator
def login_required(f):# ตรวจสอบว่ามีการ login หรือไม่ เป็น decorator
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
    top_played = SoundPost.query.order_by(SoundPost.play_count.desc()).limit(3).all()
    # แสดงเสียงที่มีคะแนนสูงสุด
    top_rated = SoundPost.query.all()
    top_rated = sorted(top_rated, key=lambda x: x.average_rating, reverse=True)[:3]
    # แสดงเสียงล่าสุด
    latest = SoundPost.query.order_by(SoundPost.created_at.desc()).limit(3).all()
    
    return render_template('index.html', 
                         top_played=top_played,
                         top_rated=top_rated,
                         latest=latest)

@app.route('/register', methods=['GET', 'POST'])
def register():# หน้า register
    form = RegisterForm()
    if form.validate_on_submit():# press submit
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=username).first(): #if have
                flash('Username นี้ถูกใช้งานแล้ว', 'danger')
                return redirect(url_for('register'))
        if User.query.filter_by(email=email).first(): #if have
                flash('Email นี้ถูกใช้งานแล้ว', 'danger')
                return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # hash password
        new_user = User(username=username, email=email, password=hashed_password) # create new row in user
        db.session.add(new_user)
        db.session.commit() # commit transaction
            
        flash('ลงทะเบียนสำเร็จ กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/top-rate')
def top_rate():#    หน้า top rate
    top_rated = SoundPost.query.all()
    top_rated = sorted(top_rated, key=lambda x: x.average_rating, reverse=True)
    return render_template('top_rate.html', top_rate_sounds=top_rated)
    

@app.route('/mostplayed')
def most_played():# หน้า most played
    most_played_sounds = SoundPost.query.order_by(SoundPost.play_count.desc()).all()
    return render_template('most_played.html', top_played_sounds=most_played_sounds)

@app.route('/latestupload')
def latest_uploads(): # หน้า latest upload
    latest = SoundPost.query.order_by(SoundPost.created_at.desc()).all()
    return render_template('latest_uploads.html',latest = latest)

@app.route('/login',methods=['GET', 'POST'])
def login():# หน้า login
    form = LoginForm()
    if form.validate_on_submit(): # ถ้ามีการกด submit
        #เอาข้อมูลมาจาก form แล้วทำการเข้าสู่ session ถ้าข้อมูลถูกต้อง
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

@login_required
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ออกจากระบบสำเร็จ', 'success')
    return redirect(url_for('login'))
 
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():# หน้า new post เอาไว้ create
    form = SoundPostForm()
    categories = Category.query.all()
    if not categories: # ถ้าไม่มี category ใดๆ ใน database
        default_categories = ["Music", "Podcast", "Nature Sounds", "Instrumental", "ASMR"]
        for name in default_categories:
            db.session.add(Category(name=name))
        db.session.commit()
        categories = Category.query.all()  # reload categories after adding default ones
    form.category.choices = [(c.id, c.name) for c in categories]
    if form.validate_on_submit():  # check when press button submit
        if not form.sound_file.data:
            flash('Sound file is required!', 'danger')
            return render_template('create_post.html', form=form)
        
        file = form.sound_file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # create path to save file
        file.save(file_path)
        
        post = SoundPost(  # create new post
            title=form.title.data,
            description=form.description.data,
            file_path=filename,
            user_id=session['user_id'],
            category_id=form.category.data
        )
        db.session.add(post)  # add post to database
        db.session.commit()  # commit changes
        
        flash('Your sound has been posted!', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):# หน้า post
    post = SoundPost.query.get_or_404(post_id) # ดึงข้อมูล post จาก id
    comment_form = CommentForm()
    rating_form = RatingForm()
    if request.method == 'POST' and 'user_id' in session: # check if user is logged in and there is a POST request
        # Check if this is a comment submission
        if comment_form.validate_on_submit(): # ถ้ามีการส่งคอมเม้น
            comment = Comment(
                content=comment_form.content.data,
                user_id=session['user_id'],
                post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('post', post_id=post_id)) # ยืนยันการเปลี่ยนแปลง
        
        # Check if this is a rating submission
        if rating_form.validate_on_submit(): # ถ้ามีการส่งคะแนน
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
            return redirect(url_for('post', post_id=post_id)) # ยืนยันการเปลี่ยนแปลง

    return render_template('post.html',  # แสดงหน้า post
                         post=post,
                         comment_form=comment_form,
                         rating_form=rating_form)


    
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    posts = SoundPost.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(): # หน้า edit profile
    user = User.query.get(session['user_id']) # ดึงข้อมูล user จาก session
    form = ProfileForm(obj=user) # ดึงข้อมูล user มาใส่ใน form
    if form.validate_on_submit():# กด submitt
        if form.profile_image.data: #   ถ้ามีการอัพโหลดรูปภาพใหม่
            image_file = secure_filename(form.profile_image.data.filename)
            form.profile_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
            user.profile_image = image_file
        user.about = form.about.data
        db.session.commit() # ยืนยันการเปลี่ยนแปลง db
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', form=form)

@app.route('/increment_play_count/<int:post_id>', methods=['POST'])
def increment_play_count(post_id):# เพิ่มจำนวนการเล่นเสียง โดยกำหนดใน html ว่าถ้าเล่นครับ 30 % เมื่อไร่ให้นับว่าเป็นการเล่น 1 ครั้ง
    post = SoundPost.query.get_or_404(post_id)
    post.play_count += 1
    db.session.commit()
    return jsonify(success=True, play_count=post.play_count) # ส่งค่ากลับไปให้ javascript ทำการแสดงผล

@app.route('/post/delete/<int:post_id>', methods=['GET','POST'])
@login_required
def delete_post(post_id): #     ลบ post
    post = SoundPost.query.get_or_404(post_id)
    if post.user_id != session['user_id']: # ตรวจสอบว่าเป็นเจ้าของ post หรือไม่
        flash('Unauthorized action', 'danger')
        return redirect(url_for('profile'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('profile'))


@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id): # หน้า edit post
    post = SoundPost.query.get_or_404(post_id) # ดึงข้อมูล post จาก id
    if post.user_id != session['user_id']:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('index'))
    
    form = SoundPostForm(obj=post)
    categories = Category.query.all() # ดึงข้อมูล category ทั้งหมด
    form.category.choices = [(c.id, c.name) for c in categories]# สร้าง list ของ category ทั้งหมด
    
    if form.validate_on_submit():# on press submit
        post.title = form.title.data
        post.description = form.description.data
        post.category_id = form.category.data
        if form.sound_file.data:# ถ้ามีการอัพโหลดไฟล์ใหม่
            file = form.sound_file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            post.file_path = filename
        db.session.commit() # บันทึกการเปลี่ยนแปลง
        flash('Post updated successfully', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_post.html', form=form, post=post)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)