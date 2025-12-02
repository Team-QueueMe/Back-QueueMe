from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user, todo 
from db import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="QueueMe User & Todo Service",
    description="유저 인증 및 할 일 관리 API",
    version="1.0.0"
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