from domain.apps.models import App
from interface.dto.app_dto import AppRequest, AppResponse


class AppMapper:
    @staticmethod
    def to_domain(user_id: str, req: AppRequest) -> App:
        return App(
            app_name=req.app_name,
            description=req.description,
            keywords=req.keywords,
            creator=user_id,
        )

    @staticmethod
    def to_response(app: App) -> AppResponse:
        return AppResponse(
            id=str(app.id),
            app_name=app.app_name,
            description=app.description,
            keywords=app.keywords,
            creator=app.creator,
            updater=app.updater,
            created_at=app.created_at.isoformat(),
            updated_at=app.updated_at.isoformat() if app.updated_at else None,
        )
