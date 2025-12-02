from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db import models, schema, database, crud
from configs.config import settings

bearer_scheme = HTTPBearer()

async def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 실패",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = creds.credentials 
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        user_id: str = payload.get("sub") 
        if user_id is None:
            raise credentials_exception
        
        return int(user_id)
            
    except JWTError:
        raise credentials_exception