import databases
from dependency_injector import containers, providers

from services.application_service import ApplicationService
from services.environment_service import EnvironmentService
from services.variable_service import VariableService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    database = providers.Singleton(
        databases.Database,
        url=config.db.connection_string
    )

    var_service = providers.Factory(
        VariableService,
        database=database,
    )

    env_service = providers.Factory(
        EnvironmentService,
        database=database,
        var_service=var_service
    )

    app_service = providers.Factory(
        ApplicationService,
        database=database,
        env_service=env_service
    )
