from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# from fastapi_utils.tasks import repeat_every

# from src.github_api import get_github_repos_by_login, update_stats

import src.api.protocols
from src.api import protocols, post
from src.dependencies import get_engine
from src.errors import (
    NotFoundError,
    NoContentError,
    DatabaseError,
    BadRequestError,
    ValidationError
)
# from src.post.service import StatService
# from src.user.service import UserService
from src.post.service import PostService


def get_application() -> FastAPI:
    application = FastAPI(
        title='Fulltext searching machine',
        description="""
Полнотекстовый поиск в базе данных.\n
PostgreSQL + ElasticSearch""",
        version='1.0.0',
        contact={
            "name": "Igor Potemkin",
            "email": "ipotemkin@rambler.ru",
        },
        docs_url="/",  # TODO comments
    )

    # application.include_router(users.router)
    application.include_router(post.router)

    engine = get_engine()

    # user_service = UserService(engine)
    # application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    #
    post_service = PostService(engine)
    application.dependency_overrides[protocols.PostServiceProtocol] = lambda: post_service

    return application


app = get_application()


@app.on_event("startup")
# @repeat_every(seconds=60 * 60 * 24)  # sets an interval for updating DB
async def on_startup():
    ...

    # TODO This code should be refactored
    # engine = get_engine()
    # stat_service = StatService(engine)
    # user_service = UserService(engine)
    # _users = user_service.get_all()
    # for user in _users:
    #     repos = await get_github_repos_by_login(user.login)
    #     update_stats(user.id, repos, stat_service)


# exception handlers
@app.exception_handler(404)
@app.exception_handler(NotFoundError)
def not_found_error(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.exception_handler(NoContentError)
def no_content_error(request: Request, exc: NoContentError):
    return JSONResponse(status_code=204, content={"message": "No Content"})


@app.exception_handler(DatabaseError)
def database_error(request: Request, exc: DatabaseError):
    return JSONResponse(status_code=400, content={"message": "Database Error"})


@app.exception_handler(BadRequestError)
def bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"message": "Bad Request"})


@app.exception_handler(ValidationError)
def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"message": "Validation Error"})
