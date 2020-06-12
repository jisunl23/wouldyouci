from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from movies import models


nori_korean = analyzer(
    'nori_korian',
    tokenizer='nori_tokenizer',
)


@registry.register_document
class MoviesDocument(Document):

    class Index:
        name = 'search_movies'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
        analyzer = nori_korean

    class Django:
        model = models.Movie
        fields = ['id', 'name', 'summary']
