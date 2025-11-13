from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    # google 소셜 로그인할때 보내주는 sub id 저장하는 필드임 
    google_id = Column(String, unique=True, index=True)
    