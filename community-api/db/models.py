from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    # google 소셜 로그인할때 보내주는 sub id 저장하는 필드임 
    google_id = Column(String, unique=True, index=True)

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    # user table 외래키로 참조 
    owner_id = Column(Integer, ForeignKey("user.id")) 
    
    message = Column(String)
    daily_progress_percentage = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정 
    owner = relationship("User", back_populates="posts")