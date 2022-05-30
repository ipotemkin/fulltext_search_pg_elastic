import sqlalchemy as sa
from elasticsearch import Elasticsearch

from src.database import DatabaseSettings, create_database_url
from src.errors import ElasticError


def get_engine():

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True,
    )
    return engine


def get_search_machine():
    try:
        es = Elasticsearch("http://localhost:9200")
        if not es.ping():
            raise ElasticError
    except Exception:
        raise ElasticError
    return es
