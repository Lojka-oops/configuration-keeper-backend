from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import change_history_schemas
from services.change_history_service import ChangeHistoryService
from containers import Container


router = APIRouter(tags=['history'])


@router.get("/history/{entity_type}/{entity_id}", response_model=change_history_schemas.ChangeHistoryListSchema)
@inject
async def get_history(
    entity_type: str,
    entity_id: int,
    page: int = 1,
    per_page: int = 10,
    change_hostory_service: ChangeHistoryService = Depends(Provide[Container.change_history_service])
) -> Response:
    """Gets history of entity by its type and id

    """

    total_count = await change_hostory_service.get_count(entity_type, entity_id)
    entity_history = await change_hostory_service.get_list(
        entity_type, 
        entity_id,
        page, 
        per_page
    )
    
    return {"total_count": total_count, "data": entity_history}
