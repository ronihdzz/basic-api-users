from fastapi import status
from models import User
from api.v1.schemas import (
    SignupUserSchema,
    RetrieveUserSchema,
    TokenSchema,
    ResponseSignupUserSchema,
    TokenTypeConstant,
)
from api.v1.repositories import UserRepository
from api.v1.internal_codes import UserInternalCodes
from api.v1.exeptions import ApiUserExceptions
from api.v1.utils.password import PasswordUtils
from api.v1.utils.jwt import JwtUtils
from api.v1.schemas import (
    TokenSchema,
    TokenTypeConstant
)
from api.v1.utils.jwt import JwtUtils
from api.v1.schemas import (
    TokenDataSchema,
    CreateLoginUserSchema,
    ResponseLoginUserSchema
)

class SignupUserService:
    
    def create_user(self, user: SignupUserSchema)-> ResponseSignupUserSchema:
        existing_user = UserRepository.get_user_by_name_or_email(user.username, user.email)
        if existing_user:
            raise ApiUserExceptions(
                status_code_http=status.HTTP_400_BAD_REQUEST,
                error_code=UserInternalCodes.ALREADY_REGISTERED,
                message="Username already registered"
            )
        hashed_password = PasswordUtils.hash_password(user.password)
        user_created = UserRepository.create_user( 
            user=User(
                username=user.username,
                hashed_password=hashed_password,
                email=user.email
            )
        )
        # Create token
        token_data = TokenDataSchema(user_id=user_created.id)
        token_data = token_data.model_dump(mode="json")
        token = JwtUtils.create_access_token(data=token_data)
    
        # Create response
        user_retrieve_schema = RetrieveUserSchema(id=user_created.id, username=user_created.username, email=user_created.email)
        token_schema = TokenSchema(access_token=token, token_type=TokenTypeConstant.BEARER)
        response_signup_user_schema = ResponseSignupUserSchema(user=user_retrieve_schema, token=token_schema)
        return response_signup_user_schema
    
class LoginUserService:
    
    def login_user(self, user: CreateLoginUserSchema)-> ResponseLoginUserSchema:
        user_found = UserRepository.get_user_by_name(user.username)
        if not user_found:
            raise ApiUserExceptions(
                status_code_http=status.HTTP_400_BAD_REQUEST,
                error_code=UserInternalCodes.USER_NOT_FOUND,
                message="User not found"
            )
        if not PasswordUtils.verify_password(user.password, user_found.hashed_password):
            raise ApiUserExceptions(
                status_code_http=status.HTTP_400_BAD_REQUEST,
                error_code=UserInternalCodes.AUTHENTICATION_FAILED,
                message="Incorrect username or password"
            )
        # Create token
        token_data = TokenDataSchema(user_id=user_found.id)
        token_data = token_data.model_dump(mode="json")
        token = JwtUtils.create_access_token(data=token_data)
    
        # Create response
        user_retrieve_schema = RetrieveUserSchema(id=user_found.id, username=user_found.username, email=user_found.email)
        token_schema = TokenSchema(access_token=token, token_type=TokenTypeConstant.BEARER)
        response_login_user_schema = ResponseLoginUserSchema(user=user_retrieve_schema, token=token_schema)
        return response_login_user_schema

