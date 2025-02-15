from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# กำหนดโมเดล User
class User(db.Model):
    __tablename__ = 'users'  # ชื่อตารางในฐานข้อมูล

    # คอลัมน์ต่าง ๆ
    id = db.Column(db.Integer, primary_key=True)  # คอลัมน์ ID (Primary Key)
    username = db.Column(db.String(80), unique=True, nullable=False)  # ชื่อผู้ใช้ (ต้องไม่ซ้ำและไม่เป็นค่าว่าง)
    email = db.Column(db.String(120), unique=True, nullable=False)  # อีเมล (ต้องไม่ซ้ำและไม่เป็นค่าว่าง)
    password = db.Column(db.String(256), nullable=False)  # รหัสผ่าน (ต้องไม่เป็นค่าว่าง)
    failed_attempts = db.Column(db.Integer, default=0)  # จำนวนครั้งที่ล็อกอินผิด (ค่าเริ่มต้นเป็น 0)

    # ฟังก์ชันสำหรับตั้งรหัสผ่าน (เข้ารหัส)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    # ฟังก์ชันสำหรับตรวจสอบรหัสผ่าน
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # ฟังก์ชันสำหรับแสดงข้อมูลเมื่อพิมพ์ออบเจกต์
    def __repr__(self):
        return f'<User {self.username}>'