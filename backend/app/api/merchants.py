from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import httpx
from app.config import settings
from app.schemas import MerchantListResponse, MerchantItem, CommonResponse

router = APIRouter()


async def fetch_amap_pois(
    keywords: str,
    longitude: float,
    latitude: float,
    radius: int = 3000,
    sort_type: str = "distance"
) -> dict:
    """调用高德地图POI搜索API"""
    if not settings.AMAP_API_KEY:
        raise HTTPException(status_code=500, detail="高德地图API Key未配置")

    url = "https://restapi.amap.com/v5/place/around"

    params = {
        "key": settings.AMAP_API_KEY,
        "keywords": keywords,
        "location": f"{longitude},{latitude}",
        "radius": radius,
        "show_fields": "business,photos,children"
    }

    if sort_type == "distance":
        params["sort"] = "distance"
    elif sort_type == "rating":
        params["sort"] = "rating"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()


@router.get("/merchants/list", response_model=CommonResponse)
async def get_nearby_merchants(
    category_id: int = Query(..., description="菜系分类ID"),
    longitude: float = Query(..., description="经度"),
    latitude: float = Query(..., description="纬度"),
    sort_type: str = Query("distance", description="排序方式: distance/rating"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    radius: int = Query(3000, ge=100, le=50000, description="搜索半径(米)")
):
    from app.database import SessionLocal
    from app.models import FoodCategory

    db = SessionLocal()
    try:
        # 获取分类关键词
        category = db.query(FoodCategory).filter(FoodCategory.id == category_id).first()
        if not category:
            return CommonResponse(code=404, message="分类不存在")

        keywords = category.keyword if category.keyword else category.name

        # 调用高德地图API
        amap_data = await fetch_amap_pois(keywords, longitude, latitude, radius, sort_type)

        if amap_data.get("status") != "1":
            return CommonResponse(code=500, message="获取商家数据失败")

        pois = amap_data.get("pois", [])

        # 转换为商家列表
        merchants = []
        for poi in pois:
            # 过滤评分过低的商家
            rating = float(poi.get("biz_ext", {}).get("rating", 0))
            if rating < 3.0:
                continue

            merchant = MerchantItem(
                id=poi.get("id", ""),
                name=poi.get("name", ""),
                cover_image=poi.get("photos", [{}])[0].get("url") if poi.get("photos") else None,
                rating=rating,
                review_count=int(poi.get("biz_ext", {}).get("rating_num", 0)),
                avg_price=int(poi.get("biz_ext", {}).get("cost", 0)),
                distance=int(float(poi.get("distance", 0))),
                address=poi.get("address", ""),
                business_status=1 if poi.get("biz_ext", {}).get("open_time") else 0,
                tags=poi.get("type", "").split(";")[:3]
            )
            merchants.append(merchant)

        # 二次排序（如果API排序不满足需求）
        if sort_type == "distance":
            merchants.sort(key=lambda x: (x.distance, -x.rating))
        elif sort_type == "rating":
            merchants.sort(key=lambda x: (-x.rating, -x.review_count))

        # 分页
        total = len(merchants)
        start = (page - 1) * page_size
        end = start + page_size
        page_merchants = merchants[start:end]

        return CommonResponse(data={
            "total": total,
            "list": [m.__dict__ for m in page_merchants]
        })

    finally:
        db.close()


@router.get("/merchants/{merchant_id}", response_model=CommonResponse)
async def get_merchant_detail(merchant_id: str):
    if not settings.AMAP_API_KEY:
        raise HTTPException(status_code=500, detail="高德地图API Key未配置")

    url = "https://restapi.amap.com/v5/place/detail"

    params = {
        "key": settings.AMAP_API_KEY,
        "id": merchant_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        amap_data = response.json()

    if amap_data.get("status") != "1":
        return CommonResponse(code=500, message="获取商家详情失败")

    pois = amap_data.get("pois", [])
    if not pois:
        return CommonResponse(code=404, message="商家不存在")

    poi = pois[0]
    biz_ext = poi.get("biz_ext", {})

    return CommonResponse(data={
        "id": poi.get("id", ""),
        "name": poi.get("name", ""),
        "cover_image": poi.get("photos", [{}])[0].get("url") if poi.get("photos") else None,
        "rating": float(biz_ext.get("rating", 0)),
        "review_count": int(biz_ext.get("rating_num", 0)),
        "avg_price": int(biz_ext.get("cost", 0)),
        "distance": int(float(poi.get("distance", 0))),
        "address": poi.get("address", ""),
        "business_status": 1 if biz_ext.get("open_time") else 0,
        "tags": poi.get("type", "").split(";")[:3],
        "phone": biz_ext.get("phone"),
        "business_hours": biz_ext.get("open_time")
    })
