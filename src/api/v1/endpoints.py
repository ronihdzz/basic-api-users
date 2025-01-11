from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from models import User
from schemas import (
    SignupUserSchema,
    RetrieveUserSchema,
    TokenSchema,
    ResponseSignupUserSchema,
    TokenTypeConstant,
    ResponseLoginUserSchema,
    CreateLoginUserSchema,
)
from utils import create_access_token, get_current_user, authenticate_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from settings import settings
from db import get_db


router = APIRouter(prefix="/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=ResponseSignupUserSchema)
def create_user(user: SignupUserSchema, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = pwd_context.hash(user.password)

    db_user = User(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token(data={"sub": str(db_user.id)})
    
    token_schema = TokenSchema(access_token=token, token_type=TokenTypeConstant.BEARER)
    user_retrieve_schema = RetrieveUserSchema(id=db_user.id, username=db_user.username, email=db_user.email)
    response_signup_user_schema = ResponseSignupUserSchema(user=user_retrieve_schema, token=token_schema)
    
    return response_signup_user_schema


@router.post("/login", response_model=ResponseLoginUserSchema)
def login_for_access_token(user: CreateLoginUserSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    token_schema = TokenSchema(access_token=access_token, token_type=TokenTypeConstant.BEARER)
    user_retrieve_schema = RetrieveUserSchema(id=user.id, username=user.username, email=user.email)
    response_login_user_schema = ResponseLoginUserSchema(user=user_retrieve_schema, token=token_schema)
    return response_login_user_schema


@router.post("/login-swagger", include_in_schema=False)
def login_swagger(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    response = {"access_token": access_token, "token_type": "bearer"}
    return response


@router.get("/me", response_model=RetrieveUserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    retrieve_user_schema = RetrieveUserSchema(id=current_user.id, username=current_user.username, email=current_user.email)
    return retrieve_user_schema


@router.delete("/me", response_model=RetrieveUserSchema)
def delete_user_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    retrieve_user_schema = RetrieveUserSchema(id=current_user.id, username=current_user.username, email=current_user.email)
    db.delete(current_user)
    db.commit()
    return retrieve_user_schema
