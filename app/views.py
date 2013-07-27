from flask import render_template, flash, redirect, request
from app import app
from forms import LoginForm, SignupForm
from models import db

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
            return '[1] Create a new user [2] sign in the user [3] redirect to the user\'s profile'
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign in',
        form = form)
