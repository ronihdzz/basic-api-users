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

class EdificioCreateSchema(BaseModel):
    nombre: str
    latitud: str
    longitud: str

class TipoSalonCreateSchema(BaseModel):
    name: str
    cuestionarios_activos: List[str] = [None]

class SalonCreateSchema(BaseModel):
    edificio_id: str
    type_salon_id: str

class PreguntaSchema(BaseModel):
    pregunta: str
    tipo_pregunta: str
    opciones: Optional[Dict[str, List[str]]] = None

class CuestionarioCreateSchema(BaseModel):
    autor: str
    nombre: str
    preguntas: list[PreguntaSchema]

class CuestionarioFirebaseSchema(BaseModel):
    autor: str
    nombre: str
    preguntas: dict[str, PreguntaSchema]

class RespuestaCreateSchema(BaseModel):
    cuestionario_id: str
    salon_id: str
    usuario_id: str
    pregunta_id: str
    payload: Dict[str, Optional[str]]
    fecha: str
