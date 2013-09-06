from migrate.versioning import api
from config import DATABASE_URI, MIGRATE_REPO

api.upgrade(DATABASE_URI, MIGRATE_REPO)
print 'Current database version: ' + str(api.db_version(DATABASE_URI, MIGRATE_REPO))
