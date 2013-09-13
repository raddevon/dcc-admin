from flask import render_template, flash, redirect, request, session, url_for
from flask.ext.login import current_user
from app import app, db, models
from app import perms
from forms import RoleForm
from flask.ext.permissions.models import Role


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
@perms.user_is('admin')
def admin():
    users = models.User.query.all()
    forms = {user.id: RoleForm(formdata=None, id=user.id, roles=[role.id for role in user.roles])
             for user in users}

    if request.method == "POST":
        current_id = int(request.form['id'])
        forms[current_id] = RoleForm(
            id=current_id, roles=[(role.id for role in user.roles) for user in users if user.id == current_id])
        current_form = forms[current_id]

        if current_form.validate():
            u = models.User.query.get(current_form.id.data)
            u.roles = [Role.query.get(role)
                       for role in current_form.roles.data]
            db.session.commit()
            flash('Roles updated for {}'.format(u))
            return redirect(url_for('admin'))

    return render_template('admin.html', users=users, forms=forms)
