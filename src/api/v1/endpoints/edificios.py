from fastapi import APIRouter, HTTPException
from schemas import BuildingCreateSchema
from api.v1.repositories import FirebaseRepository
import uuid

router = APIRouter()


#################################
# Edificios
#################################

@router.post("/buildings")
def create_building(building: BuildingCreateSchema):
    building_id = str(uuid.uuid4())
    FirebaseRepository.insert_building(building_id, building.model_dump())
    return {"id": building_id, **building.model_dump()}

@router.get("/buildings/{building_id}")
def get_building(building_id: str):
    building = FirebaseRepository.get_building(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building no encontrado")
    return building
