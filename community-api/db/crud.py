from sqlalchemy.orm import Session
from . import models, schema
from sqlalchemy import cast, Date, or_, and_
from datetime import date

def calculate_progress(db: Session, user_id: int) -> int:
    today = date.today()
    
    completed_today_count = db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        models.Task.status == "complete",
        cast(models.Task.updated_at, Date) == today 
    ).count()
    
    pending_all_count = db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        models.Task.status == "pending"
    ).count()
    
    total_active_load = completed_today_count + pending_all_count
    
    if total_active_load == 0:
        return 0

    return int((completed_today_count / total_active_load) * 100)

def create_community_post(db: Session, post: schema.PostCreate, user_id: int):
    current_progress = calculate_progress(db, user_id)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    author_name = user.name if user else "Unknown"

    db_post = models.Post(
        message=post.message,
        daily_progress_percentage=current_progress,
        owner_id=user_id,
        user_name=author_name 
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_community_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post)\
        .order_by(models.Post.created_at.desc()) \
        .offset(skip)\
        .limit(limit)\
        .all()