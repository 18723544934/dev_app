from pydantic import BaseModel, Field
from typing import List, Optional


class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: int = 0
    keyword: Optional[str] = None
    icon: Optional[str] = None
    sort: int = 0
    is_default: bool = True

    class Config:
        from_attributes = True


class DrawRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    include_custom: bool = True
    category_ids: List[int] = Field(default_factory=list, description="指定抽取范围，空则全量")


class DrawResponse(BaseModel):
    draw_id: int
    category_id: int
    category_name: str
    icon: Optional[str] = None
    draw_time: str


class MerchantItem(BaseModel):
    id: str
    name: str
    cover_image: Optional[str] = None
    rating: float = 0.0
    review_count: int = 0
    avg_price: int = 0
    distance: int = 0
    address: str = ""
    business_status: int = 1
    tags: List[str] = Field(default_factory=list)


class MerchantListResponse(BaseModel):
    total: int
    list: List[MerchantItem]


class MerchantDetailResponse(BaseModel):
    id: str
    name: str
    cover_image: Optional[str] = None
    rating: float = 0.0
    review_count: int = 0
    avg_price: int = 0
    distance: int = 0
    address: str = ""
    business_status: int = 1
    tags: List[str] = Field(default_factory=list)
    phone: Optional[str] = None
    business_hours: Optional[str] = None


class CommonResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[dict] = None
