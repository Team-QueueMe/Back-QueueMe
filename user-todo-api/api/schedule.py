from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from db import database, models, schema, crud
from configs import security

router = APIRouter()

@router.get("/schedule/recommendation", response_model=schema.RecommendationResponse)
async def recommend_schedule(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # 1. 할 일 목록 가져오기
    pending_tasks = crud.get_pending_tasks(db, current_user.id)
    
    if not pending_tasks:
        return {
            "date": date.today(),
            "message": "할 일이 없습니다.",
            "recommended_tasks": []
        }

    # 2. AI에게 추천 받기 (ID 목록만 옴)
    ai_recommendations = crud.get_ai_recommendation(pending_tasks)
    
    # 3. 결과 조합
    result_list = []
    task_map = {t.id: t for t in pending_tasks}
    
    for rec in ai_recommendations:
        t_id = rec.get("task_id")
        if t_id in task_map:
            task_obj = task_map[t_id]
            # Pydantic 모델 -> dict 변환
            # [수정] reason 추가하는 코드 삭제됨!
            task_dict = schema.TaskResponse.model_validate(task_obj).model_dump()
            result_list.append(task_dict)
            
    return {
        "date": date.today(),
        "message": "AI가 추천하는 최적의 스케줄입니다.",
        "recommended_tasks": result_list
    }

@router.post("/schedule/accept", response_model=schema.DailySummaryResponse)
async def accept_schedule(
    req: schema.AcceptScheduleRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.accept_schedule(db, current_user.id, req.ordered_task_ids)