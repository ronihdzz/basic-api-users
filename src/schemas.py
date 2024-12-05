from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional

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

class BuildingCreateSchema(BaseModel):
    name: str
    latitude: str
    longitude: str

class RoomTypeCreateSchema(BaseModel):
    name: str
    active_questionnaires: List[str] = [None]

class RoomCreateSchema(BaseModel):
    building_id: str
    room_type_id: str

class QuestionSchema(BaseModel):
    question: str
    question_type: str
    options: Optional[Dict[str, List[str]]] = None

class QuestionnaireCreateSchema(BaseModel):
    author: str
    name: str
    questions: list[QuestionSchema]

class QuestionnaireFirebaseSchema(BaseModel):
    author: str
    name: str
    questions: dict[str, QuestionSchema]

class AnswerCreateSchema(BaseModel):
    questionnaire_id: str
    room_id: str
    user_id: str
    question_id: str
    payload: Dict[str, Optional[str]]
    date: str
