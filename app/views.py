from flask import render_template, flash, redirect, request, session, url_for
from app import app
from forms import LoginForm, SignupForm
from models import db, User

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return 'User created successfully'
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign in',
        form = form)
