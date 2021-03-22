from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import applications_schemas
from services.application_service import ApplicationService
from containers import Container


router = APIRouter(tags=['applications'])


@router.post("/applications", response_model=applications_schemas.ApplicationSchema, status_code=201)
@inject
async def create(
    app: applications_schemas.ApplicationCreateSchema, 
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Creates an application

    """

    app = await app_service.create(app)
    
    return app


@router.put("/applications/{app_id}", response_model=applications_schemas.ApplicationSchema)
@inject
async def update(
    app_id: int, 
    app_data: applications_schemas.ApplicationCreateSchema,
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Updates an application by id

    """
    
    return await app_service.update(app_id=app_id, app=app_data)


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


@router.get("/applications", response_model=applications_schemas.ApplicationsListSchema)
@inject
async def get_list(
    page: int = 1,
    per_page: int = 10,
    app_service: ApplicationService = Depends(Provide[Container.app_service])
) -> Response:
    """Gets all existing applications

    """

    total_cout = await app_service.get_apps_count()
    applications = await app_service.get_apps(page, per_page)
    
    return {"total_count": total_cout, "data": applications}
