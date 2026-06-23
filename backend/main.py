from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import categories, draw, merchants
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="今天吃啥 API",
    description="餐饮决策工具后端服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api/v1", tags=["菜系分类"])
app.include_router(draw.router, prefix="/api/v1", tags=["随机抽取"])
app.include_router(merchants.router, prefix="/api/v1", tags=["商家推荐"])


@app.get("/")
async def root():
    return {"message": "今天吃啥 API 服务运行中", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
