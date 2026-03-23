from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.app.web.core.dependencies.use_cases import get_register_user, get_authenticate_user
from backend.app.application.use_cases.user.register import RegisterUser
from backend.app.application.use_cases.user.authenticate import AuthenticateUser
from backend.app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# GET маршруты для отображения модальных окон
@router.get("/auth/login", response_class=HTMLResponse)
async def login_modal(request: Request):
    return templates.TemplateResponse(
        "components/modals/auth/login_modal.html",
        {"request": request}
    )

@router.get("/auth/register", response_class=HTMLResponse)
async def register_modal(request: Request):
    return templates.TemplateResponse(
        "components/modals/auth/register_modal.html",
        {"request": request}
    )

# POST маршруты для обработки форм
@router.post("/auth/login")
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False),  # добавляем поле "запомнить меня"
    uc: AuthenticateUser = Depends(get_authenticate_user),
):
    """
    Обработка формы входа.
    При успехе - сохраняет user_id в сессии и редиректит на главную.
    """
    user = uc.execute(email=email, password=password)

    if not user:
        # Можно добавить flash сообщение об ошибке
        return RedirectResponse("/?error=invalid_credentials", status_code=303)
    
    request.session["user_id"] = user.id
    # Здесь можно учесть remember для установки длительности сессии
    return RedirectResponse("/home", status_code=303)


@router.post("/auth/register")
async def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    terms: bool = Form(...),  # добавляем поле согласия с условиями
    uc: RegisterUser = Depends(get_register_user),
):
    """
    Обработка формы регистрации.
    Проверяет совпадение паролей и создает пользователя.
    """
    if password != password2:
        return RedirectResponse("/?error=password_mismatch", status_code=303)
    
    if not terms:
        return RedirectResponse("/?error=terms_required", status_code=303)
    
    try:
        user = uc.execute(email=email, username=username, password=password)
    except ValueError as e:
        # Передаем конкретную ошибку (например, email уже существует)
        return RedirectResponse(f"/?error={str(e)}", status_code=303)
    
    request.session["user_id"] = user.id
    return RedirectResponse("/home", status_code=303)


@router.post("/auth/logout")
async def logout_form(request: Request):
    """
    Выход из системы.
    Очищает сессию и редиректит на главную.
    """
    request.session.clear()
    return RedirectResponse("/", status_code=303)