import os
from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, bcrypt
from flask_app.fourms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

def token_hex(length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])


posts = [
    {
        'author' : 'Udit Juneja',
        'title' : 'First Blog Post',
        'content' : 'First blog content',
        'date_posted' : 'April 20, 2018'
    },
    {
        'author' : 'Mayank Juneja',
        'title' : 'Second Blog Post',
        'content' : 'Second blog content',
        'date_posted' : 'April 21, 2018'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts, title = "Home")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title = 'Register', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data )
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check your information!', 'danger')
    return render_template("login.html", title = 'Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    if current_user.image_file != 'static/profile_photos/' + 'default.jpeg':
        prev_photo = os.path.join(app.root_path, 'static/profile_photos', current_user.image_file)
        os.remove(prev_photo)
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_photos', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if current_user.image_file:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_photos/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
