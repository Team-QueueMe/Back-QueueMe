from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import database, models, schema, crud
from configs import security
from typing import List

router = APIRouter()

@router.post("/community/posts", response_model=schema.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_req: schema.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    saved_post = crud.create_community_post(db=db, post=post_req, user_id=current_user.id)
    
    return schema.PostResponse(
        post_id=saved_post.id,
        user_id=current_user.google_id,  
        user_name=current_user.name,
        message=saved_post.message,
        daily_progress_percentage=saved_post.daily_progress_percentage,
        created_at=saved_post.created_at
    )

@router.get("/community/posts", response_model=List[schema.PostResponse])
async def get_posts(
    skip: int = 0, # 앞 페이지 분량 다 건너뜀 
    limit: int = 10, # 한 페이지에 보여줄 게시글 수 
    db: Session = Depends(database.get_db)
):
    posts = crud.get_community_posts(db, skip=skip, limit=limit)
    
    return [
        schema.PostResponse(
            post_id=post.id,
            user_id=post.owner.google_id, 
            user_name=post.owner.name,
            message=post.message,
            daily_progress_percentage=post.daily_progress_percentage,
            created_at=post.created_at
        ) for post in posts
    ]