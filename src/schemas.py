from pydantic import BaseModel, EmailStr
from enum import StrEnum
from uuid import UUID

class TokenTypeConstant(StrEnum):
    BEARER = "bearer"

# User
# ----------------------------------------------------------

class RetrieveUserSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    token_type: TokenTypeConstant


# Signup user
# ----------------------------------------------------------

class SignupUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class ResponseSignupUserSchema(BaseModel):
    user: RetrieveUserSchema
    token: TokenSchema



# Login
# ----------------------------------------------------------

class ResponseLoginUserSchema(BaseModel):
    user: RetrieveUserSchema
    token: TokenSchema

class CreateLoginUserSchema(BaseModel):
    username: str
    password: str
