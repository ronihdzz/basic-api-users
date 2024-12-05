import uuid
from database import firebase_session
from schemas import CuestionarioCreateSchema, CuestionarioFirebaseSchema, SalonCreateSchema, TipoSalonCreateSchema
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
    def insert_edificio(id, data):
        firebase_session.put(f'/edificios', id, data)

    @staticmethod
    def get_edificio(id):
        return firebase_session.get(f'/edificios', id)

    @staticmethod
    def insert_salon(id, data: SalonCreateSchema):
        # Validar que el edificio exista
        edificio = FirebaseRepository.get_edificio(id=data.edificio_id)
        if not edificio:
            raise HTTPException(status_code=404, detail="Edificio no encontrado")
        
        # Validar que el tipo de salón exista
        tipo_salon = FirebaseRepository.get_tipo_salon(id=data.type_salon_id)
        if not tipo_salon:
            raise HTTPException(status_code=404, detail="Tipo de salón no encontrado")
        
        # Insertar el salón si las validaciones son exitosas
        firebase_session.put(f'/salones', id, data.model_dump())

    @staticmethod
    def get_salon(id):
        return firebase_session.get(f'/salones', id)

    @staticmethod
    def insert_cuestionario(id, data: CuestionarioCreateSchema):
        cuestionario_to_save = CuestionarioFirebaseSchema(autor=data.autor, nombre=data.nombre, preguntas={})
        preguntas_with_ids = {}
        firebase_session.put(f'/cuestionarios', id, cuestionario_to_save.model_dump())
        for pregunta in data.preguntas:
            pregunta_id = str(uuid.uuid4())
            firebase_session.put(f'/cuestionarios/{id}/preguntas', pregunta_id, pregunta.model_dump())
            preguntas_with_ids[pregunta_id] = pregunta.model_dump()
        cuestionario_to_save.preguntas = preguntas_with_ids
        firebase_session.put(f'/cuestionarios', id, cuestionario_to_save.model_dump())
        return cuestionario_to_save

    @staticmethod
    def get_cuestionario(id):
        return firebase_session.get(f'/cuestionarios', id)

    @staticmethod
    def insert_respuesta(id, data):
        firebase_session.put(f'/respuestas', id, data)

    @staticmethod
    def get_respuesta(id):
        return firebase_session.get(f'/respuestas', id)

    @staticmethod
    def update_cuestionario(id, data):
        firebase_session.put(f'/cuestionarios', id, data)

    @staticmethod
    def update_salon(id, data):
        firebase_session.put(f'/salones', id, data)

    @staticmethod
    def update_respuesta(id, data):
        firebase_session.put(f'/respuestas', id, data)

    @staticmethod
    def delete_respuesta(id):
        firebase_session.delete(f'/respuestas', id)




    @staticmethod
    def insert_tipo_salon(id, data: TipoSalonCreateSchema):
        firebase_session.put(f'/tipos_salones', id, data.model_dump())

    @staticmethod
    def get_tipo_salon(id):
        return firebase_session.get(f'/tipos_salones', id)

    @staticmethod
    def update_tipo_salon(id, data: TipoSalonCreateSchema):
        firebase_session.put(f'/tipos_salones', id, data.model_dump())

    @staticmethod
    def delete_tipo_salon(id):
        firebase_session.delete(f'/tipos_salones', id)

    @staticmethod
    def get_list_tipos_salones():
        return firebase_session.get(f'/tipos_salones')