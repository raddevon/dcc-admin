from flask import render_template, flash, redirect, request, session, url_for
from flask.ext.login import current_user
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated():
        return render_template('profile.html')
    return redirect(url_for('login'))
