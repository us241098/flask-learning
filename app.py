from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from fourms import RegistrationForm, LoginForm
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6256da821325782f664b0af78bba339'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


posts = [
    {
        'auther' : 'Udit Juneja',
        'title' : 'First Blog Post',
        'content' : 'First blog content',
        'date_posted' : 'April 20, 2018'
    },
    {
        'auther' : 'Mayank Juneja',
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
    form = RegistrationForm()
    if form.validate_on_submit():
        #output = 'Account created for' + str({ form.username.data})
        #flash(output, 'success')
        flash('Account created for {name}'.format(name = {form.username.data}), 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title = 'Register', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data =='test@test.com' and form.password.data == 'test':
            flash('You have logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please check your information!', 'danger')
    return render_template("login.html", title = 'Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
