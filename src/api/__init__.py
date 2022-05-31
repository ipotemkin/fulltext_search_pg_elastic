from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import src.api.protocols
from src.api import protocols, post
from src.dependencies import get_engine
from src.errors import (
    NotFoundError,
    NoContentError,
    DatabaseError,
    BadRequestError,
    ValidationError, ElasticError
)
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

    application.include_router(post.router)

    engine = get_engine()

    post_service = PostService(engine)
    application.dependency_overrides[protocols.PostServiceProtocol] = lambda: post_service

    return application


app = get_application()


@app.on_event("startup")
async def on_startup():
    ...


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
    return JSONResponse(
        status_code=400,
        content={"message": "Database Error", "details": str(exc)}
    )


@app.exception_handler(BadRequestError)
def bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"message": "Bad Request"})


@app.exception_handler(ValidationError)
def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"message": "Validation Error"})


@app.exception_handler(ElasticError)
def elastic_error(request: Request, exc: ElasticError):
    return JSONResponse(status_code=400, content={"message": "Elastic Error"})
