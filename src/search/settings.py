from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class SearchSettings(BaseSettings):
    elasticsearch_uri: str = Field(..., env='ELASTICSEARCH_URI')
