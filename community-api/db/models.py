from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    # user table 외래키로 참조 
    owner_id = Column(Integer, index=True)
    
    message = Column(String)
    daily_progress_percentage = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

    # 관계 설정 (다른 컨테이너에 있는 서비스라 user_id 형식으로 저장하도록 함)
    user_name = Column(String)