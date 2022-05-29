from typing import List

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.future import Engine

from src.errors import (
    NotFoundError,
    NoContentError,
    BadRequestError,
    DatabaseError,
)


class BasicDAO:
    def __init__(
            self,
            engine: Engine,                 # a database engine
            model,                          # a database table model
            schema: BaseModel,              # a pydantic model to show one object
            schema_list: BaseModel = None,  # a pydantic model to show many objects
            pk_name: str = 'id'
    ):
        self._engine = engine
        self.model = model
        self.schema = schema
        self.schema_list = schema_list if schema_list else schema
        self.pk_name = pk_name

    def _execute(self, sql: str, commit=False) -> CursorResult:
        try:
            with self._engine.connect() as connection:
                result = connection.execute(sql)
                if commit:
                    connection.commit()
        except Exception as e:
            raise DatabaseError(e)

        return result

    def get_all(self, limit=10, offset=0) -> List[BaseModel]:
        query = select(self.model).order_by(self.pk_name).offset(offset).limit(limit)
        items_data = self._execute(query)
        return [self.schema_list(**item_data) for item_data in items_data]

    def get_one(self, id: int) -> BaseModel:
        query = select(self.model).where(self.model.c[self.pk_name] == id)
        item_data = self._execute(query).first()

        if not item_data:
            raise NotFoundError

        return self.schema(**item_data)

    # TODO return a new item endpoint
    def create(self, item: BaseModel) -> None:
        # breakpoint()
        query = insert(self.model).values(**item.dict(exclude_unset=True))
        # query = insert(self.model).values(**item.dict(exclude_none=True))
        self._execute(query, commit=True)

    def update(self, pk: int, item: BaseModel) -> BaseModel:
        if not item:
            raise NoContentError

        if (
            self.pk_name in item.__dict__
            and item.__dict__[self.pk_name]
            and pk != item.__dict__[self.pk_name]
        ):
            raise BadRequestError

        query = (
            update(self.model).
            where(self.model.c.id == pk).
            values(**item.dict(exclude_unset=True))
        )

        self._execute(query, commit=True)
        return self.get_one(pk)

    # updates records, which meet 'filter_d', creates a record from 'item' if such records don't exist.
    def update_or_create(self, filter_d: dict, item: BaseModel) -> None:
        data_to_update = self.filter(filter_d)
        if data_to_update:
            for item_to_update in data_to_update:
                self.update(item_to_update.__dict__[self.pk_name], item)
        else:
            self.create(item)

    def delete(self, pk: int) -> None:
        query = delete(self.model).where(self.model.c[self.pk_name] == pk)
        self._execute(query, commit=True)

    # to search with a dictionary; example {"column name": "searching SUBstring"}
    def search(self, filter_d: dict) -> List[BaseModel]:
        query = select(self.model)
        for key, value in filter_d.items():
            query = query.filter(self.model.c[key].ilike(f'%{value}%'))
        res = self._execute(query)
        return [self.schema_list(**item) for item in res]

    # to filter with a dictionary; example {"column name": "searching string"} - a strict search
    def filter(self, filter_d: dict) -> List[BaseModel]:
        query = select(self.model).filter_by(**filter_d)
        res = self._execute(query)
        return [self.schema_list(**item) for item in res]
