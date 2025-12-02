from sqlalchemy.orm import Session
from . import models, schema

def create_community_post(db: Session, post: schema.PostCreate, user_id: int):
    db_post = models.Post(
        message=post.message,
        daily_progress_percentage=post.daily_progress_percentage,
        owner_id=user_id,
        user_name=post.user_name
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