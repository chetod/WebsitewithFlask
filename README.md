# 📢 SoundShare - เว็บแชร์เสียงในชีวิตประจำวัน

ยินดีต้อนรับสู่ **SoundShare** 🎵 เว็บแอปพลิเคชันที่พัฒนาด้วย **Flask** ที่ช่วยให้ผู้ใช้สามารถ **อัปโหลด แชร์ คอมเมนต์ และให้คะแนน** เสียงต่างๆ ที่พบในชีวิตประจำวัน ไม่ว่าจะเป็นเสียงนกร้อง เสียงรถติด หรือแม้แต่เสียงดนตรีที่แต่งขึ้นเอง

---
## โครงสร้างโปรเจกต์
- `forms.py` - จัดการฟอร์มที่ใช้ในแอปพลิเคชัน
- `noteapp.py` - ไฟล์หลักที่สร้างและกำหนดเส้นทาง (routes)
- `models.py` - กำหนดโครงสร้างฐานข้อมูล

## ฟอร์มหลัก
- **RegisterForm** - สมัครสมาชิก (username, email, password)
- **LoginForm** - เข้าสู่ระบบ (username, password)
- **SoundPostForm** - โพสต์ไฟล์เสียง (title, description, category, sound_file)
- **CommentForm** - แสดงความคิดเห็น
- **RatingForm** - ให้คะแนน (1-5)
- **ProfileForm** - จัดการโปรไฟล์ (about, profile_image)

## database
- **User** - เก็บข้อมูลผู้ใช้
- **Category** - หมวดหมู่ของโพสต์
- **SoundPost** - โพสต์ไฟล์เสียง, play count, average rating
- **Comment** - ความคิดเห็นของผู้ใช้
- **Rating** - การให้คะแนนโพสต์

## Routes สำคัญ
- `/` - หน้าแรก (Top Played, Top Rated, Latest Posts)
- `/register` - สมัครสมาชิก
- `/login` - เข้าสู่ระบบ
- `/logout` - ออกจากระบบ
- `/post/new` - สร้างโพสต์ใหม่
- `/post/<int:post_id>` - ดูโพสต์
- `/profile` - ดูโปรไฟล์
- `/profile/edit` - แก้ไขโปรไฟล์
- `/increment_play_count/<int:post_id>` - เพิ่ม play count
- `/post/delete/<int:post_id>` - ลบโพสต์
- `/post/edit/<int:post_id>` - แก้ไขโพสต์
---

## 📌 Features (ฟีเจอร์หลัก)

✅ **Upload Sounds** - อัปโหลดเสียงที่คุณต้องการแชร์  
💬 **Comment System** - แสดงความคิดเห็นใต้โพสต์เสียง  
⭐ **Rating System** - ให้คะแนนเสียงที่คุณชอบ  
🔥 **Top Rated Sounds** - แสดงเสียงที่ได้คะแนนสูงสุด  
🎧 **Most Played Sounds** - แสดงเสียงที่มีการเล่นมากที่สุด  
🔐 **User Authentication** - ระบบสมัครสมาชิก & ล็อกอิน  
🛠️ **User Profiles** - โปรไฟล์ส่วนตัวสำหรับผู้ใช้  

---

## 🏗️ Project Structure (โครงสร้างโปรเจ็กต์)

```
FLASKASSIGN/
│── SimpleWebApp/
│   ├── instance/
│   │   ├── soundshare.db        # ฐานข้อมูล SQLite (จำเป็นต้องกดรันก่อนถึงจะโผล่)
│   ├── static/                  # ไฟล์ Static (CSS, JS, Images) (จำเป็นต้องกดรันก่อนถึงจะโผล่)
│   │   ├── css/                 # Stylesheets
│   │   ├── uploads/             # โฟลเดอร์เก็บไฟล์เสียง
│   ├── templates/               # ไฟล์ HTML Templates
│   │   ├── base.html            # แม่แบบหลักของเว็บ
│   │   ├── index.html           # หน้าแรก
│   │   ├── login.html           # หน้า Login
│   │   ├── register.html        # หน้า Register
│   │   ├── profile.html         # หน้าโปรไฟล์
│   │   ├── post.html            # หน้าดูรายละเอียดเสียง และกดเล่นเพลงได้
│   │   ├── create_post.html     # หน้าสร้างโพสต์เสียง
│   │   ├── edit_post.html       # หน้าแก้ไขโพสต์เสียง
│   │   ├── edit_profile.html    # หน้าแก้ไขโปรไฟล์
│   │   ├── latest_uploads.html  # แสดงเสียงที่อัปโหลดล่าสุด
│   │   ├── most_played.html     # แสดงเสียงที่มีการเล่นเยอะที่สุด
│   │   ├── top_rate.html        # แสดงเสียงที่ได้รับคะแนนสูงสุด
│   ├── forms.py                 # จัดการฟอร์มสำหรับ Authentication & Uploads
│   ├── models.py                # โมเดลฐานข้อมูล
│   ├── noteapp.py               # Flask Application หลัก
│   ├── poetry.lock              # Lock dependencies
│   ├── pyproject.toml           # จัดการ dependencies

```

---

## ⚙️ Installation Guide (วิธีติดตั้ง) และ ใช้งาน
1.git clonne https://github.com/chetod/WebsitewithFlask.git

2.cd \WebsitewithFlask\SimpleWebwithFlask

3.poetry install

4.poetry run python noteapp.py



## 🚀 Usage Guide (วิธีใช้งาน)

1. **สมัครสมาชิก** และ **ล็อกอิน**  
2. **อัปโหลดเสียง** พร้อมเพิ่มคำอธิบาย  
3. **เรียกดูเสียง** ที่คนอื่นอัปโหลด  
4. **คอมเมนต์ & ให้คะแนน** เสียงต่างๆ  
5. **แก้ไขโปรไฟล์ของคุณ** และจัดการโพสต์เสียงของตัวเอง  

---

## 🛠 Technologies Used (เทคโนโลยีที่ใช้)

- **Backend**: Flask (Python)
- **Database**: SQLite , Flask_sqlalchemy
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF


---

📢 **ขอให้สนุกกับการแชร์เสียงใน SoundShare! 🎶🚀**

