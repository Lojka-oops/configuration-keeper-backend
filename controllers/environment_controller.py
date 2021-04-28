from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import environment_schemas
from services.environment_service import EnvironmentService
from services.change_history_service import ChangeHistoryService
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
    env_data: environment_schemas.EnvironmentUpdateSchema,
    env_service: EnvironmentService = Depends(Provide[Container.env_service]),
    change_hostory_service: ChangeHistoryService = Depends(Provide[Container.change_history_service])
) -> Response:
    """Updates an environment by id

    """

    await change_hostory_service.make_history(env_id, 'environments', env_data)

    return await env_service.update(id=env_id, data=env_data)


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

    total_count = await env_service.get_count(app_id)
    envs = await env_service.get_list(app_id, page, per_page)
    
    return {"total_count": total_count, "data": envs}
