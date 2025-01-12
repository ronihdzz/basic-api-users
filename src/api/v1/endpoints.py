from fastapi import APIRouter, Depends
from models import User
from api.v1.schemas import (
    SignupUserSchema,
    RetrieveUserSchema,
    CreateLoginUserSchema,
)
from shared.responses import EnvelopeResponse, create_response_for_fast_api
from api.v1.dependencies import get_user_by_token
from api.v1.services import SignupUserService, LoginUserService
from api.v1.repositories import UserRepository
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/signup", response_model=EnvelopeResponse)
def create_user(user: SignupUserSchema):
    signup_user_service = SignupUserService()
    response_data = signup_user_service.create_user(user)
    response = create_response_for_fast_api(
        data=response_data
    )
    return response


@router.post("/login", response_model=EnvelopeResponse)
def login_for_access_token(user: CreateLoginUserSchema):
    login_user_service = LoginUserService()
    response_data = login_user_service.login_user(user)
    response = create_response_for_fast_api(
        data=response_data
    )
    return response


@router.get("/me", response_model=EnvelopeResponse)
def read_users_me(current_user: User = Depends(get_user_by_token)):
    retrieve_user_schema = RetrieveUserSchema(id=current_user.id, username=current_user.username, email=current_user.email)
    response = create_response_for_fast_api(
        data=retrieve_user_schema
    )
    return response


@router.delete("/me", response_model=EnvelopeResponse)
def delete_user_me(current_user: User = Depends(get_user_by_token)):
    retrieve_user_schema = RetrieveUserSchema(id=current_user.id, username=current_user.username, email=current_user.email)
    UserRepository.delete_user(current_user)
    response = create_response_for_fast_api(
        data=retrieve_user_schema
    )
    return response

# Swagger
# ------------------------------------------------------------------------------------

@router.post("/login-swagger", include_in_schema=False)
def login_swagger(user: OAuth2PasswordRequestForm = Depends()):
    login_user_service = LoginUserService()
    login_user_schema = CreateLoginUserSchema(username=user.username, password=user.password)
    response_data = login_user_service.login_user(login_user_schema)
    token = response_data.token.access_token
    token_type = response_data.token.token_type
    response = {"access_token": token, "token_type": token_type}
    return response
