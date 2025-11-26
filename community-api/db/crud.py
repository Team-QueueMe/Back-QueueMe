from sqlalchemy.orm import Session
from . import models, schema

def get_user_by_google_id(db: Session, google_id: str):
    return db.query(models.User).filter(models.User.google_id == google_id).first()

def create_user_with_google(db: Session, name: str, email: str, google_id: str):
    db_user = models.User(
        email=email,
        name=name,
        google_id=google_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_community_post(db: Session, post: schema.PostCreate, user_id: int):
    db_post = models.Post(
        message=post.message,
        daily_progress_percentage=post.daily_progress_percentage,
        owner_id=user_id
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