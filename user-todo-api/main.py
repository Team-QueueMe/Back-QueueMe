from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import timedelta
from configs import security
import logging

from api import user, todo 
from db import database, models

logger = logging.getLogger("uvicorn")
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = database.SessionLocal()
    try:
        master_email = "master@test.com"
        master_user = db.query(models.User).filter(models.User.email == master_email).first()
        
        if not master_user:
            master_user = models.User(
                email=master_email,
                name="개발용마스터계정",
                google_id="master_key_12345"
            )
            db.add(master_user)
            db.commit()
            db.refresh(master_user)
            logger.info(f"개발용 마스터 유저 생성 완료 (ID: {master_user.id})")
        
        expire = timedelta(days=365)
        token = security.create_access_token(data={"sub": str(master_user.id)}, expires_delta=expire)
        
        logger.info("\n" + "="*60)
        logger.info("[개발용 마스터 토큰]")
        logger.info(f"->{token}")
        logger.info("="*60 + "\n")
        
    except Exception as e:
        logger.info(f"마스터 토큰 생성 실패: {e}")
    finally:
        db.close()
    
    yield


app = FastAPI(
    title="QueueMe User & Todo Service",
    description="유저 인증 및 할 일 관리 API",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://localhost:8001", #커뮤니티 서비스 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],      
    allow_headers=["*"],      
)

app.include_router(
    user.router, 
    prefix="/api",
    tags=["Authentication/Users"]
)

app.include_router(
    todo.router,
    prefix="/api",
    tags=["Todo tasks"]
)

@app.get("/")
def read_root():
    return {
        "message": "QueueMe API (User/Todo Service)",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }