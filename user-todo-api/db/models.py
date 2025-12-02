from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
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

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    name = Column(String, nullable=False) 
    description = Column(String, nullable=True)
    priority = Column(String, default="normal")
    category = Column(String, default="etc")     
    due_date = Column(Date, nullable=False)      

    status = Column(String, default="pending")
    
    created_at = Column(DateTime, default=datetime.now)

    owner = relationship("User", back_populates="tasks")