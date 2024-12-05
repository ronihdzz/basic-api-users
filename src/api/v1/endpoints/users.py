from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserCreateSchema
from utils import create_access_token, get_current_user, authenticate_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from settings import settings
from api.v1.repositories import FirebaseRepository

router = APIRouter(prefix="/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#################################
# Users
#################################

@router.post("")
def create_user(user: UserCreateSchema):
    existing_user = FirebaseRepository.get_user(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = pwd_context.hash(user.password)
    
    user_data ={
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    FirebaseRepository.insert_user(
        user.username,
        user_data
    )
    user_data.pop("hashed_password")
    return user_data

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt_expiration_minutes)
    access_token = create_access_token(
        data={"sub": str(user["username"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    # current_user.pop("hashed_password")
    return current_user

@router.delete("/me")
def delete_user_me(current_user = Depends(get_current_user)):
    FirebaseRepository.delete_user(current_user["username"])
    return {"detail": "User deleted"}

