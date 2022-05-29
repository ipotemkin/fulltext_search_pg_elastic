from sqlalchemy.future import Engine

from src.dao.basic import BasicDAO
from src.database.tables import posts
from .models import PostRequestV1, PostResponseV1, PostListResponseV1


class PostService(BasicDAO):
    def __init__(
            self,
            engine: Engine,
            model=posts,
            schema=PostResponseV1,
            schema_list=PostListResponseV1
    ):
        super().__init__(engine, model, schema, schema_list=schema_list)
