from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# กำหนดโมเดล User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # คอลัมน์ ID (Primary Key)
    username = db.Column(db.String(80), unique=True, nullable=False)  # ชื่อผู้ใช้ (ต้องไม่ซ้ำและไม่เป็นค่าว่าง)
    email = db.Column(db.String(120), unique=True, nullable=False)  # อีเมล (ต้องไม่ซ้ำและไม่เป็นค่าว่าง)
    password = db.Column(db.String(256), nullable=False)  # รหัสผ่าน (ต้องไม่เป็นค่าว่าง)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # วันที่สร้าง (ค่าเริ่มต้นคือวันที่ปัจจุบัน)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('SoundPost', backref='category', lazy=True)

class SoundPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200), nullable=False)
    play_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('sound_post.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5 stars
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('sound_post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)