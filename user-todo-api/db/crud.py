from sqlalchemy.orm import Session
import google.generativeai as genai
from datetime import date
from sqlalchemy import cast, Date, or_, and_
from . import models, schema
import json 
import random
from configs.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_pending_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        models.Task.status == "pending"
    ).all()


def get_ai_recommendation(tasks):
    

    generation_config = genai.types.GenerationConfig(
        temperature=1.0 
    )

    model = genai.GenerativeModel('gemini-2.5-flash',generation_config=generation_config)
    
    tasks_data = [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "priority": t.priority,
            "due_date": str(t.due_date),
            "category": t.category,
            "created_at": str(t.created_at)
        } for t in tasks
    ]

    strategies = [
        "Focus strictly on 'DEADLINE' (due_date). The closest deadline must be first.",
        "Focus strictly on 'PRIORITY' (urgent > high > normal > low). Ignore deadlines slightly if needed.",
        "Focus on 'FRESHNESS'. Do the most recently created tasks first to keep momentum.",
        "Focus on 'CLEARING BACKLOG'. Do the oldest created tasks first to clean up the list.",
        "Use a 'BALANCED' approach. Mix urgent tasks with some easy low-priority wins."
    ]
    
    # 랜덤으로 전략 하나 뽑기
    current_strategy = random.choice(strategies)

    prompt = f"""
    You are a smart task manager. Analyze the tasks and suggest a recommended execution order.
    
    [IMPORTANT]
    Today's Scheduling Strategy: "{current_strategy}"
    Please sort the tasks strictly according to this strategy.
    
    Tasks: {json.dumps(tasks_data)}
    
    Output MUST be a valid JSON array of objects with 'task_id' ONLY. No explanations.
    Example: [{{ "task_id": 1 }}, {{ "task_id": 3 }}]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        print(f"적용된 전략: {current_strategy}")
        return json.loads(text)
    except Exception as e:
        print(f"AI Error: {e}")
        return []


def accept_schedule(db: Session, user_id: int, ordered_ids: list[int]):
    for index, task_id in enumerate(ordered_ids):
        task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.owner_id == user_id
        ).first()
        
        if task:
            # 0,1,2.. 순서대로 저장토록 함 
            task.display_order = index
            
    db.commit()
    
    from datetime import date
    return get_daily_summary_data(db, user_id, date.today())


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
            models.Task.status == "pending",
            and_(
                models.Task.status == "complete",
                cast(models.Task.updated_at, Date) == target_date
            )
        )
    ).order_by(models.Task.display_order.asc()).all()

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