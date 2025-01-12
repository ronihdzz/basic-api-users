from shared.internal_errors import BaseInternalError,Error

class UserInternalCodes(BaseInternalError):
    GENERAL_ERROR = Error(
        code=2000,
        description="General error api Users"
    )
    ALREADY_REGISTERED = Error(
        code=2001,
        description="User already registered"
    )
    AUTHENTICATION_FAILED = Error(
        code=2002,
        description="Password or username incorrect"
    )
    USER_NOT_FOUND = Error(
        code=2003,
        description="User not found"
    )
    TOKEN_ERROR = Error(
        code=2004,
        description="Token has expired or is invalid"
    )
    
    