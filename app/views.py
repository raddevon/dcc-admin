from flask import render_template, flash, redirect, request, session, url_for
from app import app
from forms import LoginForm, SignupForm
from models import db, User


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email

            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html',
                                   title='Login',
                                   form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email=session['email']).first()

    if not user:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')
