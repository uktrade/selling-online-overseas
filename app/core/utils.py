from django.db import connection, connections
from django.core import serializers
from django.db.models import Count


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


def delete_model_duplicates(Model, unique_attr):
    """
    Utility for migrations, if a field of a model is made unique, this will remove any duplicates already in the
    database.  It is aggressive, and will not re-link any foreign keys, they will be lost.  It simply removes all
    but one of the models that have clashing unqiue attributes
    """

    _filter = {"{0}__count__gt".format(unique_attr): 1}
    duplicates = Model.objects.values(unique_attr).annotate(Count(unique_attr)).order_by().filter(**_filter)
    for duplicate in duplicates:
        name = duplicate[unique_attr]
        count = duplicate["{0}__count".format(unique_attr)]
        model_to_delete = Model.objects.filter(name=name)[count - 1:]
        for model in model_to_delete:
            model.delete()


def fix_model_index(Model):
    with connection.cursor() as cursor:
        table_name = Model._meta.db_table
        sql = "SELECT setval('{0}_id_seq', COALESCE((SELECT MAX(id)+1 FROM {0}), 1), false)".format(table_name)
        cursor.execute(sql)
