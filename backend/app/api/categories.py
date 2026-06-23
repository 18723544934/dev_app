from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import FoodCategory
from app.schemas import CategoryResponse, CommonResponse

router = APIRouter()


@router.get("/categories", response_model=CommonResponse)
async def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(FoodCategory).order_by(FoodCategory.sort, FoodCategory.id).all()
    category_list = [
        {
            "id": cat.id,
            "name": cat.name,
            "parent_id": cat.parent_id,
            "keyword": cat.keyword,
            "icon": cat.icon,
            "sort": cat.sort,
            "is_default": cat.is_default
        }
        for cat in categories
    ]
    return CommonResponse(data={"list": category_list})


@router.get("/categories/{category_id}", response_model=CommonResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(FoodCategory).filter(FoodCategory.id == category_id).first()
    if not category:
        return CommonResponse(code=404, message="分类不存在")
    return CommonResponse(data={
        "id": category.id,
        "name": category.name,
        "parent_id": category.parent_id,
        "keyword": category.keyword,
        "icon": category.icon,
        "sort": category.sort,
        "is_default": category.is_default
    })
