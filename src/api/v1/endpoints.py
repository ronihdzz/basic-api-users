from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PreguntaSchema, UserRetrieveSchema, UserCreateSchema, Token, EdificioCreateSchema, SalonCreateSchema, CuestionarioCreateSchema, RespuestaCreateSchema
from utils import create_access_token, get_current_user, authenticate_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from settings import settings
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#################################
# Users
#################################

@router.post("/users/")
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

@router.get("/users/me/")
def read_users_me(current_user = Depends(get_current_user)):
    # current_user.pop("hashed_password")
    return current_user

@router.delete("/users/me/")
def delete_user_me(current_user = Depends(get_current_user)):
    FirebaseRepository.delete_user(current_user["username"])
    return {"detail": "User deleted"}

#################################
# Edificios
#################################
@router.post("/edificios/")
def create_edificio(edificio: EdificioCreateSchema):
    edificio_id = str(uuid.uuid4())
    FirebaseRepository.insert_edificio(edificio_id, edificio.dict())
    return {"id": edificio_id, **edificio.dict()}

@router.get("/edificios/{edificio_id}")
def get_edificio(edificio_id: str):
    edificio = FirebaseRepository.get_edificio(edificio_id)
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    return edificio

# Salones

@router.post("/salones/")
def create_salon(salon: SalonCreateSchema):
    salon_id = str(uuid.uuid4())
    FirebaseRepository.insert_salon(salon_id, salon)
    return {"id": salon_id, **salon.model_dump()}

@router.get("/salones/{salon_id}")
def get_salon(salon_id: str):
    salon = FirebaseRepository.get_salon(salon_id)
    if not salon:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return salon

@router.post("/salones/{salon_id}/cuestionarios/{cuestionario_id}")
def add_cuestionario_to_salon(salon_id: str, cuestionario_id: str):
    salon = FirebaseRepository.get_salon(salon_id)
    if not salon:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    
    cuestionario = FirebaseRepository.get_cuestionario(cuestionario_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    salon['cuestionarios_activos'] = salon.get('cuestionarios_activos', [])
    if cuestionario_id not in salon['cuestionarios_activos']:
        salon['cuestionarios_activos'].append(cuestionario_id)
        FirebaseRepository.update_salon(salon_id, salon)
    
    return {"detail": "Cuestionario agregado al salón"}

#################################
# Cuestionarios
#################################

@router.post("/cuestionarios/")
def create_cuestionario(cuestionario: CuestionarioCreateSchema):
    cuestionario_id = str(uuid.uuid4())
    response = FirebaseRepository.insert_cuestionario(cuestionario_id, cuestionario)
    return {"id": cuestionario_id, **response.model_dump()}

@router.get("/cuestionarios/{cuestionario_id}")
def get_cuestionario(cuestionario_id: str):
    cuestionario = FirebaseRepository.get_cuestionario(cuestionario_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    return cuestionario

@router.post("/cuestionarios/{cuestionario_id}/preguntas/")
def add_pregunta_to_cuestionario(cuestionario_id: str, pregunta: PreguntaSchema):
    cuestionario = FirebaseRepository.get_cuestionario(cuestionario_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    pregunta_id = str(uuid.uuid4())
    cuestionario['preguntas'] = cuestionario.get('preguntas', {})
    cuestionario['preguntas'][pregunta_id] = pregunta.dict()
    FirebaseRepository.update_cuestionario(cuestionario_id, cuestionario)
    return {"id": pregunta_id, **pregunta.dict()}

@router.delete("/cuestionarios/{cuestionario_id}/preguntas/{pregunta_id}")
def delete_pregunta_from_cuestionario(cuestionario_id: str, pregunta_id: str):
    cuestionario = FirebaseRepository.get_cuestionario(cuestionario_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    if pregunta_id not in cuestionario['preguntas']:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada en el cuestionario")
    
    del cuestionario['preguntas'][pregunta_id]
    FirebaseRepository.update_cuestionario(cuestionario_id, cuestionario)
    return {"detail": "Pregunta eliminada"}

#################################
# Respuestas
#################################

@router.post("/respuestas/")
def create_respuesta(respuesta: RespuestaCreateSchema):
    respuesta_id = str(uuid.uuid4())
    FirebaseRepository.insert_respuesta(respuesta_id, respuesta.dict())
    return {"id": respuesta_id, **respuesta.dict()}

@router.put("/respuestas/{respuesta_id}")
def update_respuesta(respuesta_id: str, respuesta: RespuestaCreateSchema):
    existing_respuesta = FirebaseRepository.get_respuesta(respuesta_id)
    if not existing_respuesta:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    FirebaseRepository.update_respuesta(respuesta_id, respuesta.dict())
    return {"detail": "Respuesta actualizada"}

@router.delete("/respuestas/{respuesta_id}")
def delete_respuesta(respuesta_id: str):
    existing_respuesta = FirebaseRepository.get_respuesta(respuesta_id)
    if not existing_respuesta:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    FirebaseRepository.delete_respuesta(respuesta_id)
    return {"detail": "Respuesta eliminada"}

