from typing import Optional
from fastapi import APIRouter, HTTPException
from schemas import QuestionSchema, QuestionnaireCreateSchema, AnswerCreateSchema
from api.v1.repositories import FirebaseRepository
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter()



#################################
# Cuestionarios
#################################

@router.post("/questionnaires")
def create_questionnaire(questionnaire: QuestionnaireCreateSchema):
    questionnaire_id = str(uuid.uuid4())
    response = FirebaseRepository.insert_questionnaire(questionnaire_id, questionnaire)
    return {"id": questionnaire_id, **response.model_dump()}

@router.get("/questionnaires")
def get_cuestionario(questionnaire_id: Optional[str] = None):
    if questionnaire_id:
        cuestionario = FirebaseRepository.get_questionnaire(questionnaire_id)
        if not cuestionario:
            raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
        return cuestionario
    else:
        cuestionarios = FirebaseRepository.get_questionnaire(None)
        return cuestionarios

@router.post("/questionnaires/{questionnaire_id}/questions")
def add_question_to_questionnaire(questionnaire_id: str, question: QuestionSchema):
    questionnaire = FirebaseRepository.get_questionnaire(questionnaire_id)
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    question_id = str(uuid.uuid4())
    questionnaire['questions'] = questionnaire.get('questions', {})
    questionnaire['questions'][question_id] = question.model_dump(mode="json")
    FirebaseRepository.update_questionnaire(questionnaire_id, questionnaire)
    return {"id": question_id, **question.model_dump(mode="json")}

@router.delete("/questionnaires/{questionnaire_id}/questions/{question_id}")
def delete_question_from_questionnaire(questionnaire_id: str, question_id: str):
    questionnaire = FirebaseRepository.get_questionnaire(questionnaire_id)
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    
    if question_id not in questionnaire['questions']:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada en el cuestionario")
    
    del questionnaire['questions'][question_id]
    FirebaseRepository.update_questionnaire(questionnaire_id, questionnaire)
    return {"detail": "Pregunta eliminada"}

#################################
# Respuestas
#################################

@router.post("/answers")
def create_answer(answer: AnswerCreateSchema):
    answer_id = str(uuid.uuid4())
    FirebaseRepository.insert_answer(answer_id, answer.dict())
    return {"id": answer_id, **answer.dict()}

@router.put("/answers/{answer_id}")
def update_answer(answer_id: str, answer: AnswerCreateSchema):
    existing_answer = FirebaseRepository.get_answer(answer_id)
    if not existing_answer:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    FirebaseRepository.update_answer(answer_id, answer.dict())
    return {"detail": "Respuesta actualizada"}

@router.delete("/respuestas/{respuesta_id}")
def delete_answer(answer_id: str):
    existing_answer = FirebaseRepository.get_answer(answer_id)
    if not existing_answer:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    FirebaseRepository.delete_answer(answer_id)
    return {"detail": "Respuesta eliminada"}
