from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class FoodCategory(Base):
    __tablename__ = "food_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="分类名称")
    parent_id = Column(Integer, default=0, comment="父分类ID，0为一级分类")
    keyword = Column(String(200), comment="地图检索关键词（逗号分隔）")
    icon = Column(String(255), comment="分类图标URL")
    sort = Column(Integer, default=0, comment="排序权重")
    is_default = Column(Boolean, default=True, comment="是否默认启用")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")


class DrawHistory(Base):
    __tablename__ = "draw_history"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    category_id = Column(Integer, nullable=False, comment="抽中的分类ID")
    category_name = Column(String(50), nullable=False, comment="分类名称快照")
    longitude = Column(Float, comment="抽取时经度")
    latitude = Column(Float, comment="抽取时纬度")
    create_time = Column(DateTime, server_default=func.now(), comment="抽取时间")


class UserCategory(Base):
    __tablename__ = "user_category"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    category_name = Column(String(50), nullable=False, comment="自定义分类名")
    keyword = Column(String(200), comment="检索关键词")
    weight = Column(Integer, default=10, comment="抽取权重，默认10")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
