from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.service import auth_backend, fastapi_users, google_oauth_client, SECRET

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent / 'templates')

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/user",
    tags=["user"],
)


@router.get("/auth/set_new_password/{token}", tags=["auth"])
async def reset_password_form(request: Request):
    return templates.TemplateResponse("reset_password_form.html", {"request": request})
