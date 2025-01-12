from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from shared.exceptions import BaseApiRestException
from shared.responses import create_response_for_fast_api
from shared.internal_errors import BaseInternalError

class ErrorResponseMiddleware(BaseHTTPMiddleware):
    def _init_(self, app):
        super()._init_(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:  # noqa: BLE001
            internal_error = BaseInternalError.UNKNOW
            error_message = None
            error_data = None
            status_code_http = status.HTTP_500_INTERNAL_SERVER_ERROR
            if isinstance(e, HTTPException):
                error_data = {"detail": str(e.detail)}
                status_code_http = e.status_code
            elif isinstance(e, BaseApiRestException):
                error_data = e.data
                error_message = e.message
                status_code_http = e.status_code_http
                internal_error = e.error_code
            else:
                error_data = {"detail": str(e)}
                status_code_http = status.HTTP_500_INTERNAL_SERVER_ERROR

            return create_response_for_fast_api(
                status_code_http=status_code_http,
                data=error_data,
                error_code=internal_error,
                message=error_message
            )