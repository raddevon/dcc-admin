from flask import render_template, flash, redirect, request, session, url_for, send_file, make_response
from flask.ext.login import current_user
from app import app, db, models
from app import perms
import json
from forms import RoleForm
from flask.ext.permissions.models import Role
from flask.ext.permissions.decorators import user_is, user_has


@app.route('/<path:path>')
@app.route('/')
def index(path=None):
    if app.debug:
        return make_response(open('app/templates/index.html').read())
    return send_file('app/templates/index.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated():
        return render_template('profile.html')
    return redirect(url_for('login'))


# @app.route('/users', methods=['GET', 'POST'])
# @user_is('admin')
# def admin():
#     with app.test_client() as api:
#         users = json.loads(api.get('api/users/').data)
#     forms = {uid: RoleForm(formdata=None, id=uid, roles=[role['id'] for role in user['roles']])
#              for uid, user in users.iteritems()}
#     print forms['3'].hidden_tag()

#     if request.method == "POST":
#         current_id = int(request.form['id'])
#         forms[current_id] = RoleForm(
#             id=current_id, roles=[(role['id'] for role in user.roles) for user in users if uid == current_id])
#         current_form = forms[current_id]

#         if current_form.validate():
#             u = models.User.query.get(current_form.id.data)
#             u.roles = [Role.query.get(role)
#                        for role in current_form.roles.data]
#             db.session.commit()
#             flash('Roles updated for {}'.format(u))
#             return redirect(url_for('admin'))

#     return render_template('admin.html', users=users, forms=forms)


@app.route('/nodes', methods=['GET', 'POST'])
@user_has('manage_nodes')
def nodes():
    return render_template('nodes.html')
