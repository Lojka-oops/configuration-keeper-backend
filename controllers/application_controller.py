from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import application_schemas
from services.application_service import ApplicationService
from services.change_history_service import ChangeHistoryService
from containers import Container


router = APIRouter(tags=['applications'])


@router.post("/applications", response_model=application_schemas.ApplicationSchema, status_code=201)
@inject
async def create(
    app: application_schemas.ApplicationCreateSchema, 
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Creates an application

    """

    app = await app_service.create(app)
    
    return app


@router.put("/applications/{app_id}", response_model=application_schemas.ApplicationSchema)
@inject
async def update(
    app_id: int, 
    app_data: application_schemas.ApplicationCreateSchema,
    app_service: ApplicationService = Depends(Provide[Container.app_service]),
    change_hostory_service: ChangeHistoryService = Depends(Provide[Container.change_history_service])
) -> Response:
    """Updates an application by id

    """
    
    old_app_data = await app_service.get_one(app_id)
    await change_hostory_service.make_history(app_id, 'Application', app_data, old_app_data)

    return await app_service.update(app_id, app_data)


@router.delete("/applications/{app_id}", status_code=200)
@inject
async def delete(
    app_id: int,
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Deletes an application by id

    """

    await app_service.delete(app_id=app_id)
    
    return {'deleted': app_id}


@router.get("/applications", response_model=application_schemas.ApplicationsListSchema)
@inject
async def get_list(
    page: int = 1,
    per_page: int = 10,
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Gets all existing applications

    """

    total_count = await app_service.get_count()
    applications = await app_service.get_list(page, per_page)
    
    return {"total_count": total_count, "data": applications}
