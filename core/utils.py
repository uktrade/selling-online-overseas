from django.db import connections
from django.core import serializers


def safe_load_fixture(apps, fixture_path):
    if connections.databases['default']['NAME'][:4] == 'test':
        return

    original_apps = serializers.python.apps
    serializers.python.apps = apps

    with open(fixture_path, 'rb') as fixture:
        objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
        for obj in objects:
            obj.save()

    serializers.python.apps = original_apps
