from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from shared.internal_errors import BaseInternalError
import fastapi
import json 

class EnvelopeResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] | None = None
    trace_id: str | None = None

class ErrorDetailResponse(BaseModel):
    internal_error: Dict[str, Any]
    details: Dict[str, Any]

    @staticmethod
    def from_error_code(error_code: BaseInternalError, details: Optional[Dict[str, Any]] = None) -> 'ErrorDetailResponse':
        return ErrorDetailResponse(
            internal_error={
                "code": error_code.code,
                "description": error_code.description,
            },
            details=details or {}
        ).model_dump()

def create_response_for_fast_api(
    status_code_http: int = fastapi.status.HTTP_200_OK,
    data: Any = None,
    error_code: Optional[BaseInternalError] = BaseInternalError.UNKNOW,
    message: Optional[str] = None
) -> JSONResponse:
    success = 200 <= status_code_http < 300
    message = message or ("Operation successful" if success else "An error occurred")

    if isinstance(data, BaseModel):
        data = data.model_dump_json()
        data = json.loads(data)

    if not success:
        data = ErrorDetailResponse.from_error_code(error_code=error_code, details=data)

    envelope_response = EnvelopeResponse(
        success=success,
        message=message,
        data=data,
        trace_id=str(uuid.uuid4()) # TODO: change to ctx_trace_id.get()
    )
    
    return JSONResponse(
        content=envelope_response.model_dump(),
        status_code=status_code_http
    )