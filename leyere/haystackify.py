import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

ENGINES = {
    'simple': 'haystack.backends.simple_backend.SimpleEngine',
    'whoosh': 'haystack.backends.whoosh_backend.WhooshEngine',
    'elasticsearch': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'solr': 'haystack.backends.solr_backend.SolrEngine',
}


def get_engine(default='simple'):
    if 'ELASTICSEARCH_URL' in os.environ:
        return 'elasticsearch'
    elif 'WHOOSH_PATH' in os.environ:
        return 'whoosh'
    return default


class HaystackConfiguration(object):
    def __init__(self, engine):
        self.engine = engine

    def configuration(self):
        return getattr(self, 'configure_' + self.engine)()

    def configure_elasticsearch(self):
        return {
            'ENGINE': ENGINES['elasticsearch'],
            #'URL': os.getenv('ELASTICSEARCH_URL', 'http://127.0.0.1:9200/'),
            'URL': os.environ['SEARCHBOX_URL'],
            'INDEX_NAME': os.getenv('ELASTICSEARCH_INDEX_NAME', 'haystack'),
            'INCLUDE_SPELLING': True
        }

    def configure_solr(self):
        return {
            'ENGINE': ENGINES['solr'],
            'URL': os.getenv('SOLR_URL', 'http://127.0.0.1:8983/solr'),
            'INCLUDE_SPELLING': True
        }

    def configure_whoosh(self):
        return {
            'ENGINE': ENGINES['whoosh'],
            'PATH': os.getenv('WHOOSH_PATH', os.path.join(PROJECT_ROOT, 'whoosh_index')),
            'INCLUDE_SPELLING': True
        }

    def configure_simple(self):
        return {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        }


def haystackify(engine=None, default='simple'):
    engine = engine or get_engine(default)
    return HaystackConfiguration(engine).configuration()
