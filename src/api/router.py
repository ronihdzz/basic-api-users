from fastapi import APIRouter

from api.v1.endpoints import router as router_users_v1
from api.endpoints import router as healthcheck_endpoints
from settings import settings

router_healthcheck = APIRouter()
router_healthcheck.include_router(healthcheck_endpoints)

router_users = APIRouter(prefix=settings.PREFIX_API_USER, tags=["Users"])
router_users.include_router(router_users_v1)        
