import csv
import os
import argparse

from django.conf import settings
from django.core.management.base import BaseCommand
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer

from ...models import Category


class Command(BaseCommand):
    help = 'Parses categories from the taxonomy file, sets up a searchable index, and adds them to the database'

    def add_arguments(self, parser):
        parser.add_argument('--inputfile')

    def handle(self, *args, **options):
        if options['inputfile']:
            csvfilename = options['inputfile']
        else:
            csvfilename = os.path.join(settings.BASE_DIR, 'products', 'fixtures', '0005_taxonomy.csv')

        csvfile = open(csvfilename, 'rt')

        # Define the Whoosh schema and get the index directory on disk
        schema = Schema(
            category=TEXT(stored=True),
            pk=ID(stored=True),
            sub_category=TEXT(stored=True, spelling=True, analyzer=StemmingAnalyzer())
        )

        indexdir = settings.WHOOSH_INDEX_DIR

        if not os.path.exists(indexdir):
            # Create the index directory if it doesn't already exist
            os.mkdir(indexdir)

        # Get the reader for the taxonomy CSV, and the writer for the index
        reader = csv.reader(csvfile)
        writer = create_in(indexdir, schema).writer()

        for row in reader:
            # Get the top-level category name for the row
            category = row[1]

            if category == 'Mature':
                # Omit the mature category on ministerial orders, to reduce the risk of reputational damage
                continue

            # Go over all columns in the row
            for index in range(2, len(row)):
                # When you find an empty column, the PREVIOUS column was a leaf sub-category for the main category
                if row[index] == '':
                    sub_category = row[index-1]
                    break
            else:
                # At end of the row's columns without finding a blank column, it means the leaf is in the last column
                sub_category = row[index]

            if category == sub_category:
                # The sub-category IS the leaf, so get it's ID
                pk = row[0]

            # Add the category name, it's primary key, and search term (the sub-category) to the index
            writer.add_document(category=category, pk=pk, sub_category=sub_category)

        writer.commit()
