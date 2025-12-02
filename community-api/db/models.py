from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, index=True)
    
    message = Column(String)
    daily_progress_percentage = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

    user_name = Column(String)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, index=True)
    
    name = Column(String, nullable=True)        
    description = Column(String, nullable=True) 
    priority = Column(String, default="normal") 
    category = Column(String, default="etc")    
    due_date = Column(Date, nullable=True)    

    status = Column(String, default="pending")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)