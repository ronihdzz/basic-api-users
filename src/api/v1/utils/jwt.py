import jwt
from datetime import datetime, timedelta, timezone
from fastapi import status
from settings import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from api.v1.exeptions import ApiUserExceptions
from api.v1.internal_codes import UserInternalCodes

class JwtUtils:
    
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    
    @classmethod
    def validate_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
        except ExpiredSignatureError:
            raise ApiUserExceptions(
                status_code_http=status.HTTP_401_UNAUTHORIZED,
                error_code=UserInternalCodes.TOKEN_ERROR,
                message=f"{UserInternalCodes.TOKEN_ERROR.description} - {e}"
            )
        except InvalidTokenError as e:
            raise ApiUserExceptions(
                status_code_http=status.HTTP_401_UNAUTHORIZED,
                error_code=UserInternalCodes.TOKEN_ERROR,
                message=f"{UserInternalCodes.TOKEN_ERROR.description} - {e}"
            )
        except jwt.JWTError as e:
            raise ApiUserExceptions(
                status_code_http=status.HTTP_401_UNAUTHORIZED,
                error_code=UserInternalCodes.TOKEN_ERROR,
                message=f"{UserInternalCodes.TOKEN_ERROR.description} - {e}"
            )
        return payload
        
