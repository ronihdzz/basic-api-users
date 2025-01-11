from fastapi import FastAPI
from api.v1.endpoints import router as api_router
from api.endpoints import router as index_router
from settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(index_router)
app.include_router(api_router, prefix="/v1", tags=["Users"])
