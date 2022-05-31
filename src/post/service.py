from typing import Optional

from pydantic import BaseModel
from sqlalchemy.future import Engine
from sqlalchemy import select, delete, insert, update

from src.dao.basic import BasicDAO
from src.database.tables import posts
from .models import PostRequestV1, PostResponseV1, PostListResponseV1


from src.search.service import add_to_index, query_index, remove_from_index
from ..errors import DatabaseError, NoContentError, BadRequestError


class PostService(BasicDAO):
    def __init__(
        self,
        engine: Engine,
        model=posts,
        schema=PostResponseV1,
        schema_list=PostListResponseV1,
        index="posts"
):
        super().__init__(engine, model, schema, schema_list=schema_list)
        self.index = index

    def create(self, item: BaseModel) -> int:
        with self._engine.connect() as conn:
            with conn.begin() as trans:
                try:
                    query = (
                        insert(self.model)
                        .returning(self.model)
                        .values(**item.dict(exclude_unset=True))
                    )
                    result = conn.execute(query)
                    new_post = self.schema(**result.fetchone())
                    add_to_index(self.index, new_post)
                    trans.commit()
                    print(new_post.id)  # TODO remove before release
                    return new_post.id

                except Exception as e:
                    trans.rollback()
                    raise DatabaseError(e)

    def update(self, pk: int, item: BaseModel) -> BaseModel:
        if not item:
            raise NoContentError

        if (
                self.pk_name in item.__dict__
                and item.__dict__[self.pk_name]
                and pk != item.__dict__[self.pk_name]
        ):
            raise BadRequestError

        with self._engine.connect() as conn:
            with conn.begin() as trans:
                try:
                    query = (
                        update(self.model).
                        returning(self.model).
                        where(self.model.c.id == pk).
                        values(**item.dict(exclude_unset=True))
                    )
                    res = conn.execute(query)
                    updated_post = self.schema(**res.fetchone())
                    add_to_index(self.index, updated_post)
                    trans.commit()
                    return updated_post

                except Exception as e:
                    trans.rollback()
                    raise DatabaseError(e)

    def delete(self, pk: int) -> None:
        with self._engine.connect() as conn:
            with conn.begin() as trans:
                try:
                    query = delete(self.model).where(self.model.c[self.pk_name] == pk)
                    conn.execute(query)
                    remove_from_index(self.index, pk)
                    trans.commit()
                except Exception as e:
                    trans.rollback()
                    raise DatabaseError(e)

    def sm_search(self, query: str, page=1, per_page=10, ordering: Optional[str] = None):
        ids, total = query_index(index=self.index, query=query, page=page, per_page=per_page)
        if total == 0:
            return []

        sql = select(self.model).where(self.model.c[self.pk_name].in_(ids)).order_by(ordering)
        items_data = self._execute(sql)
        # print(self.model.name)
        return [self.schema(**item_data) for item_data in items_data]
