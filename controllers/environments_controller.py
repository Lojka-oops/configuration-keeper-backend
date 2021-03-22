from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import environments_schemas
from services.environment_service import EnvironmentService
from containers import Container

router = APIRouter(tags=['environments'])


@router.post(
    "/environments", 
    response_model=environments_schemas.EnvironmentSchema, 
    status_code=201
)
@inject
async def create_environment(
    environment: environments_schemas.EnvironmentCreateSchema, 
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Creates an environment

    """

    environment = await env_service.create_env(environment)
    
    return environment


@router.put("/environments/{env_id}", response_model=environments_schemas.EnvironmentSchema)
@inject
async def update_environment(
    env_id: int, 
    app_data: environments_schemas.EnvironmentCreateSchema,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Updates an environment by id

    """

    return await env_service.update_env(env_id=env_id, env=app_data)


@router.delete("/environments/{env_id}", status_code=200)
@inject
async def delete_environment(
    env_id: int,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Deletes an environment by id

    """

    await env_service.delete_env(env_id=env_id)
    
    return {'deleted': env_id}


@router.get("/environments", response_model=environments_schemas.EnvironmentsListSchema)
@inject
async def get_environments(
    app_id: int,
    page: int = 1,
    per_page: int = 10,
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Gets all existing environments for application

    """

    total_cout = await env_service.get_envs_count(app_id)
    envs = await env_service.get_envs(app_id, page, per_page)
    
    return {"total_count": total_cout, "data": envs}
