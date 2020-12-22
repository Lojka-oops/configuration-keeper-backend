from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException

from controllers import apps_controller, environments_controller, \
    variables_controller, configuration_controller
from helpers import dependencies
from containers import Container

tags_metadata = [
    {
        "name": "configurations",
        "description": "Operations with configurations."
    },
    {
        "name": "applications",
        "description": "Operations with applications."
    },
    {
        "name": "environments",
        "description": "Operations with environments."
    },
    {
        "name": "variables",
        "description": "Operations with variables."
    }
]


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config/config.yaml')
    container.wire(
        modules=[
            apps_controller, 
            environments_controller, 
            variables_controller, 
            configuration_controller,
            dependencies
        ]
    )

    app = FastAPI(
        title="Configuration Keeper",
        description="""This is a project whose main idea 
            is to give developers a single place to store 
            the configurations of their applications with 
            the ability to customize them and then pull 
            them into their projects.""",
        version="0.3.0",
        openapi_tags=tags_metadata
    )
    app.container = container
    app.include_router(apps_controller.router)
    app.include_router(environments_controller.router)
    app.include_router(variables_controller.router)
    app.include_router(configuration_controller.router)

    return app


app = create_app()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(Exception)
async def internal_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": f"{exc}"}
    )


@app.on_event("startup")
async def startup() -> None:
    await app.container.database().connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.container.database().disconnect()
