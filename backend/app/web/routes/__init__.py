from fastapi import APIRouter, FastAPI
from .pages import router as pages_router
from .api.v1 import router as api_v1_router
from .public.tokens import trigger as tokens_trigger

router = APIRouter()

router.include_router(pages_router)                  # HTML pages
router.include_router(api_v1_router, prefix="/api")  # API
router.include_router(tokens_trigger.router)         # Public

def register_web_routes(app: FastAPI) -> None:
    app.include_router(router)