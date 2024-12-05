import uuid
from database import firebase_session
from schemas import QuestionnaireCreateSchema, QuestionnaireFirebaseSchema, RoomCreateSchema, RoomTypeCreateSchema
from fastapi import HTTPException
class FirebaseRepository:

    @staticmethod
    def insert_user(id, data):
        firebase_session.put(f'/users', id, data)
        
    @staticmethod       
    def get_user(id):
        return firebase_session.get(f'/users', id)
    
    @staticmethod
    def update_user(id, data):
        firebase_session.put(f'/users', id, data)

    @staticmethod
    def delete_user(id):
        firebase_session.delete(f'/users', id)

    @staticmethod
    def insert_building(id, data):
        firebase_session.put(f'/edificios', id, data)

    @staticmethod
    def get_building(id):
        return firebase_session.get(f'/edificios', id)

    @staticmethod
    def insert_room(id, data: RoomCreateSchema):
        # Validar que el edificio exista
        building = FirebaseRepository.get_building(id=data.building_id)
        if not building:
            raise HTTPException(status_code=404, detail="Edificio no encontrado")
        
        # Validar que el tipo de salón exista
        room_type = FirebaseRepository.get_room_type(id=data.room_type_id)
        if not room_type:
            raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
        
        # Insertar el salón si las validaciones son exitosas
        firebase_session.put(f'/salones', id, data.model_dump())

    @staticmethod
    def get_room(id):
        return firebase_session.get(f'/salones', id)

    @staticmethod
    def insert_questionnaire(id, data: QuestionnaireCreateSchema):
        questionnaire_to_save = QuestionnaireFirebaseSchema(autor=data.autor, nombre=data.nombre, preguntas={})
        questions_with_ids = {}
        firebase_session.put(f'/cuestionarios', id, questionnaire_to_save.model_dump())
        for question in data.questions:
            question_id = str(uuid.uuid4())
            firebase_session.put(f'/cuestionarios/{id}/preguntas', question_id, question.model_dump())
            questions_with_ids[question_id] = question.model_dump()
        questionnaire_to_save.preguntas = questions_with_ids
        firebase_session.put(f'/cuestionarios', id, questionnaire_to_save.model_dump())
        return questionnaire_to_save

    @staticmethod
    def get_questionnaire(id):
        return firebase_session.get(f'/cuestionarios', id)

    @staticmethod
    def insert_answer(id, data):
        firebase_session.put(f'/respuestas', id, data)

    @staticmethod
    def get_answer(id):
        return firebase_session.get(f'/respuestas', id)

    @staticmethod
    def update_questionnaire(id, data):
        firebase_session.put(f'/cuestionarios', id, data)

    @staticmethod
    def update_room(id, data):
        firebase_session.put(f'/salones', id, data)

    @staticmethod
    def update_answer(id, data):
        firebase_session.put(f'/respuestas', id, data)

    @staticmethod
    def delete_answer(id):
        firebase_session.delete(f'/respuestas', id)




    @staticmethod
    def insert_room_type(id, data: RoomTypeCreateSchema):
        firebase_session.put(f'/tipos_salones', id, data.model_dump())

    @staticmethod
    def get_room_type(id):
        return firebase_session.get(f'/tipos_salones', id)

    @staticmethod
    def update_room_type(id, data: RoomTypeCreateSchema):
        firebase_session.put(f'/tipos_salones', id, data.model_dump())

    @staticmethod
    def delete_room_type(id):
        firebase_session.delete(f'/tipos_salones', id)

    @staticmethod
    def get_list_room_types():
        return firebase_session.get(f'/tipos_salones')
