from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "유효하지 않은 토큰입니다."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "권한이 없습니다."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class DBConnectionError(HTTPException):
    def __init__(self, detail: str = "커넥션 실패"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
