from fastapi import APIRouter, HTTPException
from schemas import PreguntaSchema,CuestionarioCreateSchema, RespuestaCreateSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter()



#################################
# Cuestionarios
#################################

@router.post("/questionnaires")
def create_cuestionario(cuestionario: CuestionarioCreateSchema):
    cuestionario_id = str(uuid.uuid4())
    response = FirebaseRepository.insert_cuestionario(cuestionario_id, cuestionario)
    return {"id": cuestionario_id, **response.model_dump()}

@router.get("/questionnaires/{questionnaire_id}")
def get_cuestionario(questionnaire_id: str):
    cuestionario = FirebaseRepository.get_cuestionario(questionnaire_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    return cuestionario

@router.post("/questionnaires/{questionnaire_id}/questions")
def add_pregunta_to_cuestionario(questionnaire_id: str, pregunta: PreguntaSchema):
    cuestionario = FirebaseRepository.get_cuestionario(questionnaire_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    pregunta_id = str(uuid.uuid4())
    cuestionario['preguntas'] = cuestionario.get('preguntas', {})
    cuestionario['preguntas'][pregunta_id] = pregunta.model_dump(mode="json")
    FirebaseRepository.update_cuestionario(questionnaire_id, cuestionario)
    return {"id": pregunta_id, **pregunta.model_dump(mode="json")}

@router.delete("/questionnaires/{questionnaire_id}/questions/{question_id}")
def delete_pregunta_from_cuestionario(questionnaire_id: str, question_id: str):
    cuestionario = FirebaseRepository.get_cuestionario(questionnaire_id)
    if not cuestionario:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    if question_id not in cuestionario['preguntas']:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada en el cuestionario")
    
    del cuestionario['preguntas'][question_id]
    FirebaseRepository.update_cuestionario(questionnaire_id, cuestionario)
    return {"detail": "Pregunta eliminada"}

#################################
# Respuestas
#################################

@router.post("/answers")
def create_respuesta(respuesta: RespuestaCreateSchema):
    answer_id = str(uuid.uuid4())
    FirebaseRepository.insert_answer(answer_id, respuesta.dict())
    return {"id": answer_id, **respuesta.dict()}

@router.put("/answers/{answer_id}")
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
