from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/login") - для JSON API
# @router.post("/register") - для JSON API