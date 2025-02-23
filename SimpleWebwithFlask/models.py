from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# กำหนดโมเดล User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('SoundPost', backref='author', lazy=True)# สร้างความสัมพันธ์กับโพสต์
    comments = db.relationship('Comment', backref='author', lazy=True)# สร้างความสัมพันธ์กับคอมเม้นต์
    ratings = db.relationship('Rating', backref='user', lazy=True)# สร้างความสัมพันธ์กับการให้คะแนน
    about = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)

    def get_total_plays(self): # นับจำนวนการเล่นทั้งหมด
        return sum(post.play_count for post in self.posts)
    
    def get_average_rating(self):# คำนวณค่าเฉลี่ยของการให้คะแนน
        total_ratings = sum(post.average_rating for post in self.posts if post.average_rating)
        count = sum(1 for post in self.posts if post.average_rating)
        return total_ratings / count if count > 0 else 0

# กำหนดโมเดล Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('SoundPost', backref='category', lazy=True)# สร้างความสัมพันธ์กับโพสต์

# กำหนดโมเดล SoundPost
class SoundPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200), nullable=False)
    play_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # สร้างความสัมพันธ์กับผู้ใช้
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # สร้างความสัมพันธ์กับหมวดหมู่
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")  # สร้างความสัมพันธ์กับคอมเม้นต์
    ratings = db.relationship('Rating', backref='post', lazy=True, cascade="all, delete-orphan")  # สร้างความสัมพันธ์กับการให้คะแนน

    @property  # สร้างเมทอดเพื่อคำนวณค่าเฉลี่ยของการให้คะแนน
    def average_rating(self):  # คำนวณค่าเฉลี่ยของการให้คะแนน
        if not self.ratings:
            return 0
        return sum(r.value for r in self.ratings) / len(self.ratings)

# กำหนดโมเดล Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)# สร้างความสัมพันธ์กับผู้ใช้
    post_id = db.Column(db.Integer, db.ForeignKey('sound_post.id'), nullable=False)# สร้างความสัมพันธ์กับโพสต์

# กำหนดโมเดล Rating
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5 stars
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)# สร้างความสัมพันธ์กับผู้ใช้
    post_id = db.Column(db.Integer, db.ForeignKey('sound_post.id'), nullable=False)# สร้างความสัมพันธ์กับโพสต์
    created_at = db.Column(db.DateTime, default=datetime.utcnow)