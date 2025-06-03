from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.users.token_service import TokenService
from containers import Container
from domain.users.models import User

security = HTTPBearer()


@inject
async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(Provide[Container.token_service]),
) -> User:
    """
    - Authorization: Bearer <token>
    - 토큰 유효성 검사 → User 반환
    """
    user = token_service.validate_token(cred.credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # 👇 RequestContextMiddleware의 request.state에 저장
    from middleware.request_context import get_request

    request = get_request()
    request.state.user = user

    return user
