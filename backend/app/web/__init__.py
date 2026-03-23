"""
Главный инициализатор web слоя.
Объединяет все маршруты из pages, api и public.
"""
from fastapi import APIRouter, FastAPI
from .pages import router as pages_router
from .api.v1 import router as api_v1_router
from .public.tokens import trigger as tokens_trigger

# Создаем главный роутер для web слоя
router = APIRouter()

# Подключаем все маршруты
router.include_router(pages_router)                 # HTML страницы
router.include_router(api_v1_router, prefix="/api")  # API
router.include_router(tokens_trigger.router)        # Публичные


# Функция для регистрации всех маршрутов в приложении
def register_web_routes(app: FastAPI) -> None:
    app.include_router(router)