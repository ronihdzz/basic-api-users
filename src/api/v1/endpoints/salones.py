from fastapi import APIRouter, HTTPException
from schemas import TipoSalonCreateSchema, SalonCreateSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter(prefix="/classrooms")


#################################
# Salones
#################################

@router.post("/classrooms")
def create_salon(salon: SalonCreateSchema):
    classroom_id = str(uuid.uuid4())
    FirebaseRepository.insert_salon(classroom_id, salon)
    return {"id": classroom_id, **salon.model_dump()}

@router.get("/classrooms/{classroom_id}")
def get_salon(classroom_id: str):
    salon = FirebaseRepository.get_salon(classroom_id)
    if not salon:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return salon

#################################
# Tipos de salones
#################################

@router.post("/types")
def create_tipo_salon(tipo_salon: TipoSalonCreateSchema):
    classroom_type_id = str(uuid.uuid4())
    FirebaseRepository.insert_tipo_salon(classroom_type_id, tipo_salon)
    return {"id": classroom_type_id, **tipo_salon.model_dump()}

@router.get("/types/{classroom_type_id}")
def get_tipo_salon(classroom_type_id: str):
    tipo_salon = FirebaseRepository.get_tipo_salon(classroom_type_id)
    if not tipo_salon:
        raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
    return tipo_salon

@router.get("/types")
def get_list_tipos_salones():
    tipos_salones = FirebaseRepository.get_list_tipos_salones()
    return tipos_salones


@router.post("/types/{classroom_type_id}/questionnaires/{questionnaire_id}")
def add_cuestionario_to_salon(classroom_type_id: str, questionnaire_id: str):
    tipo_salon = FirebaseRepository.get_tipo_salon(classroom_type_id)
    if not tipo_salon:
        raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
    
    cuestionario = FirebaseRepository.get_cuestionario(questionnaire_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    tipo_salon['cuestionarios_activos'] = tipo_salon.get('cuestionarios_activos', [])
    if questionnaire_id not in tipo_salon['cuestionarios_activos']:
        tipo_salon['cuestionarios_activos'].append(questionnaire_id)
        FirebaseRepository.update_tipo_salon(classroom_type_id, tipo_salon)
    
    return {"detail": "Cuestionario agregado al tipo de salón"}
