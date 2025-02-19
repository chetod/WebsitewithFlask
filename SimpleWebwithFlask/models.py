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
    pass