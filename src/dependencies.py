import sqlalchemy as sa
from elasticsearch import Elasticsearch

from src.database import DatabaseSettings, create_database_url


def get_engine():

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True,
    )
    return engine


def get_search_machine():
    es = Elasticsearch("http://localhost:9200")
    return es
