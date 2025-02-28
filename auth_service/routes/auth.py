from fastapi import APIRouter, Response, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse

from schemas.user import RegisterForm, UserRole, LoginForm, OAuthForm
from schemas.oauth import YandexAuthResponse, YandexInfoResponse

from services.user import user_service
from services.jwt import token_service
from services.oauth import oauth_service

router = APIRouter()

@router.post("/auth/register")
async def register(user: RegisterForm):
    if await user_service.create_user(user_form=user, oauth=False, role=UserRole.regular):
        return Response(status_code=200)
    raise HTTPException(detail="try with another email. User already exsists!", status_code=409)

@router.post("/auth/register/admin")
async def register(user: RegisterForm):
    if await user_service.create_user(user_form=user, oauth=False, role=UserRole.admin):
        return Response(status_code=200)
    raise HTTPException(detail="try with another email. User already exsists!", status_code=409)

@router.post("/auth/login")
async def login(user: LoginForm):
    tokens = await user_service.auth_user_default(user)
    if not tokens:
        raise HTTPException(detail="Invalid email or password", status_code=401)
    response = Response()
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="strict")
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True, samesite="strict")
    return response

@router.post("/auth/refresh")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(detail="Refresh token is missing!", status_code=401)
    tokens = token_service.refresh_tokens(refresh_token=refresh_token)
    response = Response()
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="strict")
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True, samesite="strict")
    return response

@router.get("/auth/login/yandex")
async def OAuth():
    return RedirectResponse(oauth_service.AUTH_LINK)

@router.get("/auth/callback/yandex")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    token_response = oauth_service.get_tokens(code)
    user_info = oauth_service.get_user_info(access_token=token_response.access_token)
    await user_service.create_user(user_form=RegisterForm(username=user_info.username, email=user_info.email), oauth=True, role=UserRole.regular)
    tokens = await user_service.auth_user_oauth(user_info.email)
    response = Response()
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="strict")
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True, samesite="strict")
    return response