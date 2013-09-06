import imp
from migrate.versioning import api
from app import db
from config import DATABASE_URI
from config import MIGRATE_REPO

migration = MIGRATE_REPO + '/versions/%03d_migration.py' % (
    api.db_version(DATABASE_URI, MIGRATE_REPO) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(DATABASE_URI, MIGRATE_REPO)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(
    DATABASE_URI, MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)

api.upgrade(DATABASE_URI, MIGRATE_REPO)

print 'New migration saved as ' + migration
print 'Current database version: ' + str(api.db_version(DATABASE_URI, MIGRATE_REPO))
