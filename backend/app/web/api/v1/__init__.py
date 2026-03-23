from fastapi import APIRouter
from .tokens import routes as tokens_routes
from .events import routes as events_routes
from .auth import routes as auth_routes

router = APIRouter(prefix="/v1")
router.include_router(tokens_routes.router)      # /api/v1/tokens
router.include_router(events_routes.router)   # /api/v1/events
router.include_router(auth_routes.router)        # /api/v1/auth