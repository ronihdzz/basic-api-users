from fastapi import APIRouter, HTTPException
from schemas import RoomTypeCreateSchema, RoomCreateSchema
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter(prefix="/classrooms")


#################################
# Salones
#################################

@router.post("/classrooms")
def create_room(room: RoomCreateSchema):
    room_id = str(uuid.uuid4())
    FirebaseRepository.insert_room(room_id, room)
    return {"id": room_id, **room.model_dump()}

@router.get("/classrooms/{room_id}")
def get_room(room_id: str):
    room = FirebaseRepository.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return room

#################################
# Tipos de salones
#################################

@router.post("/types")
def create_room_type(room_type: RoomTypeCreateSchema):
    room_type_id = str(uuid.uuid4())
    FirebaseRepository.insert_room_type(room_type_id, room_type)
    return {"id": room_type_id, **room_type.model_dump()}

@router.get("/types/{room_type_id}")
def get_room_type(room_type_id: str):
    room_type = FirebaseRepository.get_room_type(room_type_id)
    if not room_type:
        raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
    return room_type

@router.get("/types")
def get_list_room_types():
    room_types = FirebaseRepository.get_list_room_types()
    return room_types


@router.post("/types/{room_type_id}/questionnaires/{questionnaire_id}")
def add_questionnaire_to_room(room_type_id: str, questionnaire_id: str):
    room_type = FirebaseRepository.get_room_type(room_type_id)
    if not room_type:
        raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
    
    questionnaire = FirebaseRepository.get_questionnaire(questionnaire_id)
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    room_type['active_questionnaires'] = room_type.get('active_questionnaires', [])
    if questionnaire_id not in room_type['active_questionnaires']:
        room_type['active_questionnaires'].append(questionnaire_id)
        FirebaseRepository.update_room_type(room_type_id, room_type)
    
    return {"detail": "Cuestionario agregado al tipo de salón"}
