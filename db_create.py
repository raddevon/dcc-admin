from migrate.versioning import api
from config import DATABASE_URI, MIGRATE_REPO
from app import db, app
import os.path

with app.test_request_context():
    db.create_all()

if not os.path.exists(MIGRATE_REPO):
    api.create(MIGRATE_REPO, 'database repository')
    api.version_control(DATABASE_URI, MIGRATE_REPO)
else:
    api.version_control(DATABASE_URI,
                        MIGRATE_REPO, api.version(MIGRATE_REPO))
