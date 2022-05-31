from typing import List, Optional

from fastapi import APIRouter, status, Depends, Path, Query

from src.api.protocols import PostServiceProtocol
from src.post.models import (
    PostResponseV1,
    PostRequestV1,
    PostUpdateRequestV1,
    PostListResponseV1
)

router = APIRouter(
    tags=['Posts']
)


@router.get(
    path='/v1/posts/search',
    response_model=List[PostResponseV1],
    summary='Полнотекстовый поиск',
    description='Реализует полнотекстовый поиск.'
)
async def fulltext_search(
        text: Optional[str] = Query(
            default=None, description="Введите строку для поиска"
        ),
        post_service: PostServiceProtocol = Depends(),
):
    if not text:
        return []

    return post_service.sm_search(query=text, per_page=20, ordering="created_date")


@router.get(
    path='/v1/posts',
    response_model=List[PostListResponseV1],
    summary='Посты',
    description='Возвращает список всех постов.'
)
async def get_all_posts(
        text: Optional[str] = Query(
            default=None,
            description="Введите строку для поиска"
        ),
        post_service: PostServiceProtocol = Depends(),
        limit: int = Query(default=100, ge=0),
        offset: int = Query(default=0, ge=0),
):
    if text:
        return post_service.search({"text": text})

    return post_service.get_all(limit=limit, offset=offset)


@router.get(
    path='/v1/posts/{id}',
    response_model=PostResponseV1,
    summary='Информация о посте',
    description='Возвращает информацию о посте'
)
async def get_post_by_id(
        id: int = Path(..., ge=1),
        post_service: PostServiceProtocol = Depends()
):
    return post_service.get_one(id)


@router.post(
    path='/v1/posts',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить пост',
    description='Добавляет пост.',
)
def add_post(
        post_data: PostRequestV1,
        post_service: PostServiceProtocol = Depends()
):
    post_service.create(post_data)


@router.delete(
    path='/v1/posts/{id}',
    summary='Удалить пост',
    description='Удаляет пост.'
)
def delete_post(
        id: int = Path(..., ge=1),
        post_service: PostServiceProtocol = Depends()
):
    post_service.delete(id)


@router.patch(
    path='/v1/posts/{pid}',
    response_model=PostResponseV1,
    summary='Изменить пост',
    description='Изменяет пост.'
)
def update_stats_by_id(
        post_data: PostUpdateRequestV1,
        pid: int = Path(..., ge=1),
        post_service: PostServiceProtocol = Depends(),
):
    return post_service.update(pid, post_data)
