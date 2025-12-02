from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from db import database, models, schema, crud
from configs import security

router = APIRouter()

@router.post("/tasks", response_model=schema.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_req: schema.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_task(db=db, task=task_req, user_id=current_user.id)

@router.get("/tasks", response_model=List[schema.TaskResponse])
async def read_all_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.get_all_tasks(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/tasks/{task_id}", response_model=schema.TaskResponse)
async def read_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    task = crud.get_task_by_id(db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")
    return task


@router.patch("/tasks/{task_id}/progress", response_model=schema.TaskResponse)
async def update_task_progress(
    task_id: int,
    update_req: schema.TaskUpdateStatus,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    task = crud.get_task_by_id(db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")
    
    return crud.update_task_status(db, db_task=task, status=update_req.status)


@router.get("/daily/summary", response_model=schema.DailySummaryResponse)
@router.get("/daily/summary/{target_date}", response_model=schema.DailySummaryResponse)
async def get_daily_summary(
    target_date: Optional[date] = None, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if target_date is None:
        target_date = date.today()
    
    tasks = crud.get_tasks_by_date(db, user_id=current_user.id, target_date=target_date)
    
    total_count = len(tasks)
    progress_percentage = 0
    if total_count > 0:
        completed_count = sum(1 for t in tasks if t.status == "complete")
        progress_percentage = int((completed_count / total_count) * 100)

    return schema.DailySummaryResponse(
        date=target_date,
        progress_percentage=progress_percentage,
        tasks=tasks
    )