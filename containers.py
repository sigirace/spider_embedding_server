from dependency_injector import containers, providers
from application.users.token_service import TokenService
from common.system_logger import SystemLogger
from database.mongo import get_async_mongo_client


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "interface.controller.dependency",
            "interface.controller.router",
            "middleware",
        ]
    )

    motor_client = providers.Singleton(get_async_mongo_client)
    system_logger = providers.Singleton(
        SystemLogger,
        client=motor_client,
    )
    token_service = providers.Factory(TokenService)
