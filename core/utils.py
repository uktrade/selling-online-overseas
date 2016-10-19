from django.db import connections
from django.core import serializers


def safe_load_fixture(apps, fixture_path):
    """
    This is a 'safe' fixture load during a migration.  It avoids the issue that the serializers use the latest model
    definition as in models.py, which may have extra and/or removed fields from what is 'current' in the DB at the time
    the migration is run.  So it uses the migration's apps, to change the serializers in use to be those that will work
    during the migration, and then switches them back afterwards.

    This is not necessarily futureproof, as it is allmost certainly not thread-safe or multiple-db-safe
    """

    # Do nothing if we are using the test DB (i.e. performing unit tests)
    if connections.databases['default']['NAME'][:4] == 'test':
        return

    # Story the original apps framework that django uses
    original_apps = serializers.python.apps
    # Replace it with the state of the current schema as per the migration
    serializers.python.apps = apps

    # Do our object import
    with open(fixture_path, 'rb') as fixture:
        objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
        for obj in objects:
            obj.save()

    # Reset the apps back to the original
    serializers.python.apps = original_apps
