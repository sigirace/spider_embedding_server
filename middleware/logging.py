from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from dependency_injector.wiring import Provide, inject
from common.system_logger import SystemLogger
from containers import Container


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    @inject
    async def dispatch(
        self,
        request: Request,
        call_next,
        logger: SystemLogger = Provide[Container.system_logger],
    ) -> Response:
        start = time.time()
        start_record = {
            "method": request.method,
            "path": request.url.path,
            "headers": dict(request.headers),
            "type": "START",
        }
        await logger.info(start_record)

        try:
            response = await call_next(request)

            end_record = {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "elapsed_ms": int((time.time() - start) * 1000),
                "type": "END",
            }
            await logger.info(end_record)

            return response

        except Exception as e:
            error_record = {
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "type": "ERROR",
            }
            await logger.error(error_record)
            raise
