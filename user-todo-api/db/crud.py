from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import cast, Date, or_, and_
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

def create_task(db: Session, task: schema.TaskCreate, user_id: int):
    db_task = models.Task(
        name=task.name,
        description=task.description,
        priority=task.priority,
        category=task.category,
        due_date=task.due_date,
        owner_id=user_id,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task)\
        .filter(models.Task.owner_id == user_id)\
        .order_by(models.Task.due_date.asc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_daily_tasks(db: Session, user_id: int, target_date: date):
    return db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        or_(
            models.Task.status == "pending",  # 아직 안 끝난 건 무조건 포함
            and_(
                models.Task.status == "complete",
                cast(models.Task.updated_at, Date) == target_date # 완료된 건 날짜 확인
            )
        )
    ).all()

def get_tasks_by_date(db: Session, user_id: int, target_date: date):
    return db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        cast(models.Task.created_at, Date) == target_date
    ).all()


def get_task_by_id(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

def update_task_status(db: Session, db_task: models.Task, status: str):
    db_task.status = status
    db.commit()
    db.refresh(db_task)
    return db_task

def get_daily_summary_data(db: Session, user_id: int, target_date: date):
    tasks = get_daily_tasks(db, user_id, target_date)
    
    total_count = len(tasks)
    progress_percentage = 0
    
    if total_count > 0:
        completed_count = sum(1 for t in tasks if t.status == "complete")
        progress_percentage = int((completed_count / total_count) * 100)
        
    return {
        "date": target_date,
        "progress_percentage": progress_percentage,
        "tasks": tasks
    }