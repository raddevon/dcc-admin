from migrate.versioning import api
from config import DATABASE_URI, MIGRATE_REPO

v = api.db_version(DATABASE_URI, MIGRATE_REPO)
api.downgrade(DATABASE_URI, MIGRATE_REPO, v - 1)
print 'Current database version: ' + str(api.db_version(DATABASE_URI, MIGRATE_REPO))
