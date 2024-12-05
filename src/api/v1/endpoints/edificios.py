from fastapi import APIRouter, HTTPException
from schemas import EdificioCreateSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter()


#################################
# Edificios
#################################

@router.post("/buildings")
def create_edificio(edificio: EdificioCreateSchema):
    building_id = str(uuid.uuid4())
    FirebaseRepository.insert_edificio(building_id, edificio.model_dump())
    return {"id": building_id, **edificio.model_dump()}

@router.get("/buildings/{building_id}")
def get_edificio(building_id: str):
    edificio = FirebaseRepository.get_edificio(building_id)
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    return edificio
