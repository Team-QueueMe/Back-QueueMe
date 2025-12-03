from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import community
from db import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="QueueMe Community",
    description="",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],      
    allow_headers=["*"],      
)

app.include_router(
    community.router,
    prefix="/api",
    tags=["Community"]
)

@app.get("/")
def read_root():
    return {
        "message": "QueueMe API(community)",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }