from flask import g, redirect, url_for, flash, render_template, request
from flask.ext.login import login_user, logout_user, current_user
from app import login_manager, app
from forms import LoginForm, SignupForm
from models import User, db
from flask.ext.permissions.models import Role, Ability


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.context_processor
def inject_login_form():
    form = LoginForm()
    return dict(login_form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if current_user.is_authenticated():
        return redirect(url_for('profile'))

    if request.method == 'POST' and form.validate():
        newuser = User(form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        return redirect(url_for('profile'))

    # Form does not validate
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If a user is already logged in
    if current_user.is_authenticated():
        flash('You are already logged in. To sign in as another user, first logout.')
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        login_user(user)
        flash('Login successful')
        return redirect(url_for('profile'))

    # Form does not validate
    return render_template('login.html',
                           title='Login',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
