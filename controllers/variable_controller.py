from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import variable_schemas
from services.variable_service import VariableService
from services.change_history_service import ChangeHistoryService
from containers import Container


router = APIRouter(tags=['variables'])


@router.post("/variables", response_model=variable_schemas.VariableSchema, status_code=201)
@inject
async def create(
    variable: variable_schemas.VariableCreateSchema, 
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Creates an variable

    """

    variable = await var_service.create(variable)
    
    return variable


@router.put("/variables/{var_id}", response_model=variable_schemas.VariableSchema)
@inject
async def update(
    var_id: int, 
    var_data: variable_schemas.VariableCreateSchema,
    var_service: VariableService = Depends(Provide[Container.var_service]),
    change_hostory_service: ChangeHistoryService = Depends(Provide[Container.change_history_service])
) -> Response:
    """Updates an variable by id

    """

    old_var_data = await var_service.get_one(var_id)
    await change_hostory_service.make_history(var_id, 'Variable', var_data, old_var_data)

    return await var_service.update(id=var_id, data=var_data)


@router.delete("/variables/{var_id}", status_code=200)
@inject
async def delete(
    var_id: int,
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Deletes an variable by id

    """

    await var_service.delete(var_id=var_id)
    
    return {'deleted': var_id}


@router.get("/variables", response_model=variable_schemas.VariablesListSchema)
@inject
async def get_list(
    env_id: int,
    page: int = 1,
    per_page: int = 10,
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Gets all existing variables for environment

    """

    total_cout = await var_service.get_count(env_id)
    variables = await var_service.get_list(env_id, page, per_page)
    
    return {"total_count": total_cout, "data": variables}
