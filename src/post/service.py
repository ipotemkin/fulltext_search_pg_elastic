from pydantic import BaseModel
from sqlalchemy.future import Engine

from src.dao.basic import BasicDAO
from src.database.tables import posts
from .models import PostRequestV1, PostResponseV1, PostListResponseV1
from ..search.search_mixin import SearchableMixin


# class PostService(BasicDAO, SearchableMixin):
from src.search.service import add_to_index


class PostService(BasicDAO):
    def __init__(
        self,
        engine: Engine,
        model=posts,
        schema=PostResponseV1,
        schema_list=PostListResponseV1
):
        super().__init__(engine, model, schema, schema_list=schema_list)

    def create(self, item: BaseModel) -> int:
        new_pk = super().create(item)
        add_to_index("posts", self.get_one(new_pk))
        return new_pk

    def update(self, pk: int, item: BaseModel) -> BaseModel:
        updated_post = super().update(pk, item)
        add_to_index("posts", updated_post)
        return updated_post

    def delete(self, pk: int) -> None:
        super().delete(pk)
