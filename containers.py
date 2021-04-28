import databases
from dependency_injector import containers, providers

from services.application_service import ApplicationService
from services.environment_service import EnvironmentService
from services.variable_service import VariableService
from services.change_history_service import ChangeHistoryService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    database = providers.Singleton(
        databases.Database,
        url=config.db.connection_string
    )

    var_service = providers.Factory(
        VariableService,
        database=database
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

    change_history_service = providers.Factory(
        ChangeHistoryService,
        database=database,
        app_service=app_service,
        env_service=env_service,
        var_service=var_service
    )
