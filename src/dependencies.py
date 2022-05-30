import sqlalchemy as sa
from elasticsearch import Elasticsearch

from src.database import DatabaseSettings, create_database_url
from src.errors import ElasticError
from src.search.settings import SearchSettings


def get_engine():
    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True,
    )
    return engine


def get_search_machine():
    search_settings = SearchSettings()
    es = Elasticsearch(search_settings.elasticsearch_uri)
    if not es.ping():
        raise ElasticError
    return es
