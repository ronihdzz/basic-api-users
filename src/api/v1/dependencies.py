from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from models import User
from settings import settings
from api.v1.utils.jwt import JwtUtils
from api.v1.schemas import TokenDataSchema
from api.v1.repositories import UserRepository
from api.v1.exeptions import ApiUserExceptions
from api.v1.internal_codes import UserInternalCodes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.LOGIN_SWAGGER_URL)

def get_user_by_token(token: str = Depends(oauth2_scheme))-> User:
    token_data = JwtUtils.validate_token(token)
    token_data_schema = TokenDataSchema(**token_data)
    user = UserRepository.get_user_by_id(token_data_schema.user_id)
    if not user:
        raise ApiUserExceptions(
            status_code_http=status.HTTP_400_BAD_REQUEST,
            error_code=UserInternalCodes.USER_NOT_FOUND,
            message="User not found or deleted",
        )
    return user


