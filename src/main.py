from fastapi import FastAPI
#from models import Base
#from database import engine
from api.v1.endpoints.users import router as users_router
from api.v1.endpoints.cuestionarios import router as cuestionarios_router
from api.v1.endpoints.edificios import router as edificios_router
from api.v1.endpoints.salones import router as salones_router

from api.endpoints import router as index_router
from settings import settings

#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

app.include_router(index_router)
app.include_router(users_router, prefix="/v1", tags=["Users"])
app.include_router(cuestionarios_router, prefix="/v1", tags=["Cuestionarios"])
app.include_router(edificios_router, prefix="/v1", tags=["Edificios"])
app.include_router(salones_router, prefix="/v1", tags=["Salones"])
