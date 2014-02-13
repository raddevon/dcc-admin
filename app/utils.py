from flask.ext.permissions import models as perms_models


def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


def fetch_record(Model, id):
    fetched_record = Model.query.get(id)
    if not fetched_record:
        abort(404, message="Requested record does not exist in the database.")
    return fetched_record


def fetch_role(name):
    fetched_role = perms_models.Role.query.filter_by(name=name).first()
    if not fetched_role:
        abort(404, message="Requested role does not exist in the database.")
    return fetched_role
