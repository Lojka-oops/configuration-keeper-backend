from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from schemas import configurations_schemas
from services.variable_service import VariableService
from services.environment_service import EnvironmentService
from helpers.dependencies import basic_auth
from containers import Container


router = APIRouter(tags=['configurations'])


@router.get(
    "/configurations", 
    response_model=configurations_schemas.ConfigurationSchema,
    dependencies=[Depends(basic_auth)]
)
@inject
async def get_configuration(
    code: str,
    var_service: VariableService = Depends(Provide[Container.var_service]),
    env_service: EnvironmentService = Depends(Provide[Container.env_service])
) -> Response:
    """Gets app configuration by environment unique code

    """

    environment = await env_service.get_env_by_code(code)    
    variables = await var_service.get_vars(environment['id'])

    return {'environment_name': environment['name'], 'variables': variables}
