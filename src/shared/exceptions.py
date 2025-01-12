import fastapi
from typing import Optional, Any, Dict
from loguru import logger
from shared.internal_errors import BaseInternalError

class BaseApiRestException(Exception):
    GENERAL_STATUS_CODE_HTTP = fastapi.status.HTTP_400_BAD_REQUEST
    GENERAL_ERROR_CODE = BaseInternalError.UNKNOW
    
    def __init__(self, 
                 status_code_http: int = None, 
                 error_code: BaseInternalError = None, 
                 message: Optional[str] = None, 
                 data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code_http = status_code_http if status_code_http else self.GENERAL_STATUS_CODE_HTTP
        self.error_code = error_code if error_code else self.GENERAL_ERROR_CODE
        self.data = data
        self.message = message
        logger.warning(self.__str__())
    
    def __str__(self):
        return f"[{self.status_code_http}] {self.error_code.description}: {self.message}"