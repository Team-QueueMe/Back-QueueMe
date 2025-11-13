from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user
from db import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="QueueMe Community",
    description="",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    # 프론트엔드 도메인 추가해야함!!! 
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
    tags=["Authentication & Users"]
)

@app.get("/")
def read_root():
    return {
        "message": "QueueMe API(community)",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }