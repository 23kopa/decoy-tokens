from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from backend.app.web.core.dependencies.current_user import get_current_user

router = APIRouter()

@router.get("/")
async def landing_page(request: Request, user=Depends(get_current_user)):

    if user:
        return RedirectResponse("/home", status_code=303)

    templates = request.app.state.templates

    context = {
    "request": request,
    }
    
    return templates.TemplateResponse("pages/hello.html", context)

