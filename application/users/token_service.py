from fastapi import HTTPException, status

from domain.users.models import User
from utils.jwt_utils import decode_token, JWTError


class TokenService:
    def validate_token(self, access_token: str) -> User:
        """
        1) JWT 디코딩
        2) 필수 클레임 검증
        3) User 도메인 객체 반환
        """
        try:
            decoded = decode_token(access_token)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
            ) from e

        if "user_id" not in decoded:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return User(**decoded)
