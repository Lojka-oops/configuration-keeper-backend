from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import variables_schemas
from services.variable_service import VariableService
from containers import Container


router = APIRouter(tags=['variables'])


@router.post("/variables", response_model=variables_schemas.VariableSchema, status_code=201)
@inject
async def create(
    variable: variables_schemas.VariableCreateSchema, 
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Creates an variable

    """

    variable = await var_service.create(variable)
    
    return variable


@router.put("/variables/{var_id}", response_model=variables_schemas.VariableSchema)
@inject
async def update(
    var_id: int, 
    variable_data: variables_schemas.VariableCreateSchema,
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Updates an variable by id

    """

    return await var_service.update(var_id=var_id, var=variable_data)


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


@router.get("/variables", response_model=variables_schemas.VariablesListSchema)
@inject
async def get_list(
    env_id: int,
    page: int = 1,
    per_page: int = 10,
    var_service: VariableService = Depends(Provide[Container.var_service])
) -> Response:
    """Gets all existing variables for environment

    """

    total_cout = await var_service.get_vars_count(env_id)
    variables = await var_service.get_vars(env_id, page, per_page)
    
    return {"total_count": total_cout, "data": variables}
