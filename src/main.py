from fastapi import FastAPI
from fastapi.middleware import Middleware
from api.router import router_users, router_healthcheck
from settings import settings
from shared.midllewares.envolve_pydantic import pydantic_validation_error_handler
from shared.midllewares.envolve_responses import ErrorResponseMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    middleware=[
        Middleware(ErrorResponseMiddleware)
    ]
)

app.include_router(router_healthcheck)
app.include_router(router_users)

pydantic_validation_error_handler(app)
