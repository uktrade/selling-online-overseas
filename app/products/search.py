from django.conf import settings

from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def perform_category_query(query_words):
    """
    Perform a query using the supplied words on the product category index
    """

    indexdir = settings.WHOOSH_INDEX_DIR
    ix = open_dir(indexdir)
    query = QueryParser('sub_category', ix.schema).parse(query_words)

    categories = {}
    suggestion = None

    with ix.searcher() as searcher:
        results = searcher.search(query)

        for result in results:
            if result['category'] not in categories:
                categories[result['category']] = [result['sub_category']]
            else:
                categories[result['category']] += [result['sub_category']]

        corrected = searcher.correct_query(query, query_words)
        if hasattr(corrected.query, 'text') and corrected.query.text != query_words:
            suggestion = corrected.string

    return categories, suggestion
