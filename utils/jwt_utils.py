from fastapi import HTTPException, status
from config import get_settings
from jose import ExpiredSignatureError, JWTError, jwt

from domain.users.exceptions import ExpiredToken, InvalidToken

settings = get_settings()

jwt_config = settings.jwt

ALGORITHM = jwt_config.jwt_algorithm
SECRET_KEY = jwt_config.jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_config.access_token_expires_in
REFRESH_TOKEN_EXPIRES_IN = jwt_config.refresh_token_expires_in


def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return decoded

    except ExpiredSignatureError:
        raise ExpiredToken

    except JWTError:
        raise InvalidToken

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
