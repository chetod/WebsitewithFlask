from flask import Flask, render_template, redirect, url_for, flash
from forms import RegisterForm
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
        flash('ลงทะเบียนสำเร็จ', 'success')
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)