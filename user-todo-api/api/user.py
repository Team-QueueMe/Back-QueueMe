from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from configs.config import settings
from configs import security
from db import database, models, schema, crud

router = APIRouter()

@router.get("/login/google")
async def login_google():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return RedirectResponse(url=auth_url)


@router.get("/google-auth", response_model=schema.Token)
async def auth_google_callback(request: Request, code: str, db: Session = Depends(database.get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            token_res = await client.post(token_url, data=token_data)
            token_res.raise_for_status()
            id_token_jwt = token_res.json().get("id_token")
            if not id_token_jwt:
                raise HTTPException(status_code=400, detail="id token이 google 응답에서 안보임")
        except httpx.HTTPStatusError as e:
            print(f"구글 인증 에러: {e.response.text}")
            raise HTTPException(status_code=400, detail="google로 토큰 가져오기 실패")

    try:
        id_info = id_token.verify_oauth2_token(
            id_token_jwt, 
            google_requests.Request(), 
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
        
        google_id = id_info.get("sub") 
        email = id_info.get("email")
        name = id_info.get("name")
        
        if not email or not google_id:
            raise HTTPException(status_code=400, detail="토큰이 유효하지 않습니다")

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=401, detail="유효하지 않은 google token")

    user = crud.get_user_by_google_id(db, google_id=google_id)
    
    if not user:
        user = crud.create_user_with_google(db, name=name, email=email, google_id=google_id)

    access_token = security.create_access_token(
        data={"sub": str(user.id)}
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/user", response_model=schema.User)
async def read_users_me(
    current_user: models.User = Depends(security.get_current_user)
):
    return current_user


@router.post("/logout")
async def logout(
    current_user: models.User = Depends(security.get_current_user)
):
    return JSONResponse(status_code=200, content={"message": "logout 성공"})