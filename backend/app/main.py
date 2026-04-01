from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from .core.config import settings

from .web.routes import register_web_routes
from .web.middlewares import setup_middlewares


def create_app() -> FastAPI:
    
    app = FastAPI(
        title="TokenGuard",
        version="0.1.0"
    )

    setup_middlewares(app)
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static",)
    app.mount("/media", StaticFiles(directory=str(settings.MEDIA_DIR)), name="media",)

    jinja_env = Environment(
        loader=FileSystemLoader(str(settings.TEMPLATES_DIR)),
        autoescape=True,
        cache_size=0
    )

    templates = Jinja2Templates(env=jinja_env)

    app.state.templates = templates

    templates.env.globals["use_vite"] = settings.USE_VITE
    templates.env.globals["get_current_user"] = lambda request: request.session.get("user_id")

    register_web_routes(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()


