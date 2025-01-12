from dataclasses import dataclass

@dataclass(frozen=True)
class Error:
    code: int
    description: str

class BaseInternalError:
    UNKNOW = Error(1, "Unknown Error")
    PYDANTIC_VALIDATIONS_REQUEST = Error(1000, "Failed pydantic validations on request")