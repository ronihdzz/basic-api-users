from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreateSchema(UserBase):
    password: str

class UserRetrieveSchema(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None
