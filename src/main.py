from fastapi import FastAPI
#from models import Base
#from database import engine
from api.v1.endpoints import router as api_router
from api.endpoints import router as index_router
from settings import settings

#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

app.include_router(index_router)
app.include_router(api_router, prefix="/v1", tags=["Users"])
