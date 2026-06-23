from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import random
from typing import List
from app.database import get_db
from app.models import FoodCategory, DrawHistory, UserCategory
from app.schemas import DrawRequest, CommonResponse

router = APIRouter()


def random_draw(categories: List[dict]) -> dict:
    """权重随机抽取算法"""
    total_weight = sum(cat.get("weight", 10) for cat in categories)
    random_num = random.random() * total_weight

    for cat in categories:
        random_num -= cat.get("weight", 10)
        if random_num <= 0:
            return cat
    return categories[-1]


@router.post("/draw", response_model=CommonResponse)
async def draw_category(request: DrawRequest, db: Session = Depends(get_db)):
    # 获取默认分类
    query = db.query(FoodCategory).filter(FoodCategory.is_default == True)
    if request.category_ids:
        query = query.filter(FoodCategory.id.in_(request.category_ids))
    default_categories = query.all()

    categories = []

    # 添加默认分类
    for cat in default_categories:
        categories.append({
            "id": cat.id,
            "name": cat.name,
            "keyword": cat.keyword,
            "icon": cat.icon,
            "weight": 10
        })

    # 添加用户自定义分类
    if request.include_custom:
        custom_cats = db.query(UserCategory).filter(
            UserCategory.user_id == request.user_id
        ).all()
        for cat in custom_cats:
            categories.append({
                "id": cat.id,
                "name": cat.category_name,
                "keyword": cat.keyword,
                "icon": None,
                "weight": cat.weight
            })

    if not categories:
        return CommonResponse(code=400, message="没有可抽取的分类")

    # 执行随机抽取
    result = random_draw(categories)

    # 记录抽取历史
    history = DrawHistory(
        user_id=request.user_id,
        category_id=result["id"],
        category_name=result["name"]
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return CommonResponse(data={
        "draw_id": history.id,
        "category_id": result["id"],
        "category_name": result["name"],
        "icon": result["icon"],
        "draw_time": history.create_time.strftime("%Y-%m-%d %H:%M:%S")
    })


@router.get("/draw/history/{user_id}", response_model=CommonResponse)
async def get_draw_history(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    histories = db.query(DrawHistory).filter(
        DrawHistory.user_id == user_id
    ).order_by(DrawHistory.create_time.desc()).limit(limit).all()

    history_list = [
        {
            "draw_id": h.id,
            "category_id": h.category_id,
            "category_name": h.category_name,
            "draw_time": h.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in histories
    ]

    return CommonResponse(data={"list": history_list})
