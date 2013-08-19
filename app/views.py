from flask import render_template, flash, redirect, request, session, url_for
from flask.ext.login import current_user
from app import app, db, models
from auth import user_has
from forms import RoleForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated():
        return render_template('profile.html')
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
# @user_has(['admin'])
def admin():
    users = models.User.query.all()
    forms = {user.uid: RoleForm(uid=user.uid, roles=[role.id for role in user.roles])
             for user in users}

    if request.method == "POST":
        current_form = forms[int(request.form['uid'])]

        if current_form.validate():
            u = models.User.query.get(current_form.uid.data)
            u.roles = [models.Role.query.get(x)
                       for x in current_form.roles.data]
            db.session.commit()
            flash('Roles updated for {}'.format(u))

    return render_template('admin.html', users=users, forms=forms)
