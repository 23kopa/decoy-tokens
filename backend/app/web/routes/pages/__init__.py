from fastapi import APIRouter
from .private import home as private_home
from .private import dashboard as private_dashboard
from .public import auth as public_auth
from .public import landing as public_landing

router = APIRouter()

# Публичные страницы
router.include_router(public_landing.router)     # содержит "/"
router.include_router(public_auth.router)        # содержит "/auth/login", "/auth/register"

# Приватные страницы
router.include_router(private_home.router)     # содержит "/home"
router.include_router(private_dashboard.router)  # содержит "/dashboard"