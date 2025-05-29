from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dependency_injector.wiring import Provide, inject

from application.users.token_service import TokenService
from domain.users.models import User
from containers import Container

security = HTTPBearer()


@inject
async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(Provide[Container.token_service]),
) -> User:
    """
    FastAPI Depends 사용 예:
      - Authorization: Bearer <token>
      - 성공 시 User 객체 반환, 실패 시 401 예외
    """
    return token_service.validate_token(cred.credentials)
