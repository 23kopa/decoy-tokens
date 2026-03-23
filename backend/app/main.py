from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .core.config import settings
from .web import register_web_routes

from .web.core.middlewares import setup_session_middleware

from backend.app.infrastructure.database.engine import engine, Base
from backend.app.infrastructure.database import models


def create_app() -> FastAPI:
    
    app = FastAPI(
        title="Directory Tokens",
        version="0.1.0"
    )

    setup_session_middleware(app)

    app.mount(
        "/static",
        StaticFiles(directory=str(settings.STATIC_DIR)),
        name="static",
    )

    # Base.metadata.create_all(bind=engine)

    templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

    app.state.templates = templates

    templates.env.globals["use_vite"] = settings.USE_VITE
    templates.env.globals["get_current_user"] = lambda request: request.session.get("user_id")

    register_web_routes(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()


