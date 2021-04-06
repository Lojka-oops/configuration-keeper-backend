from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import environment_schemas
from services.environment_service import EnvironmentService
from containers import Container


router = APIRouter(tags=['environments'])


@router.post(
    "/environments", 
    response_model=environment_schemas.EnvironmentSchema, 
    status_code=201
)
@inject
async def create(
    environment: environment_schemas.EnvironmentCreateSchema, 
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Creates an environment

    """

    environment = await env_service.create(environment)
    
    return environment


@router.put("/environments/{env_id}", response_model=environment_schemas.EnvironmentSchema)
@inject
async def update(
    env_id: int, 
    app_data: environment_schemas.EnvironmentCreateSchema,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Updates an environment by id

    """

    return await env_service.update(env_id=env_id, env=app_data)


@router.delete("/environments/{env_id}", status_code=200)
@inject
async def delete(
    env_id: int,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Deletes an environment by id

    """

    await env_service.delete(env_id=env_id)
    
    return {'deleted': env_id}


@router.get("/environments", response_model=environment_schemas.EnvironmentsListSchema)
@inject
async def get_list(
    app_id: int,
    page: int = 1,
    per_page: int = 10,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Gets all existing environments for application

    """

    total_cout = await env_service.get_count(app_id)
    envs = await env_service.get_list(app_id, page, per_page)
    
    return {"total_count": total_cout, "data": envs}
