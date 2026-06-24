# 开发指南

## 环境要求

### 后端
- Python 3.8+
- MySQL 5.7+
- Redis (可选，用于缓存)

### 前端
- Flutter SDK 3.0+
- Android Studio / Xcode (用于移动端调试)
- Visual Studio Code (推荐)

## 后端开发

### 项目结构说明

```
backend/
├── app/
│   ├── api/              # API路由模块
│   │   ├── categories.py # 菜系分类相关接口
│   │   ├── draw.py      # 随机抽取相关接口
│   │   └── merchants.py # 商家推荐相关接口
│   ├── models.py        # SQLAlchemy数据库模型
│   ├── schemas.py       # Pydantic数据验证模型
│   ├── config.py        # 配置管理
│   ├── database.py      # 数据库连接管理
│   └── __init__.py
├── scripts/
│   └── init_db.py      # 数据库初始化脚本
├── main.py             # FastAPI应用入口
├── requirements.txt     # Python依赖列表
└── .env               # 环境配置文件
```

### 开发流程

1. **创建虚拟环境**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate.bat  # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接和高德地图API Key
```

4. **初始化数据库**
```bash
python scripts/init_db.py
```

5. **启动开发服务器**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 添加新接口

1. 在 `app/api/` 目录下创建新模块
2. 创建路由函数并添加到 `main.py` 中
3. 在 `app/schemas.py` 中定义请求/响应模型
4. 如需数据库操作，在 `app/models.py` 中添加模型

示例：
```python
# app/api/example.py
from fastapi import APIRouter
from app.schemas import CommonResponse

router = APIRouter()

@router.get("/example", response_model=CommonResponse)
async def get_example():
    return CommonResponse(data={"message": "Hello"})
```

## 前端开发

### 项目结构说明

```
frontend/lib/
├── main.dart                 # 应用入口
├── models/                   # 数据模型
│   ├── category.dart         # 菜系分类模型
│   └── merchant.dart        # 商家模型
├── screens/                  # 页面
│   ├── home_screen.dart     # 首页（抽取页）
│   ├── merchant_list_screen.dart  # 商家列表页
│   └── all_categories_screen.dart # 全部分类页
├── services/                 # 服务层
│   └── api_service.dart    # API请求服务
├── providers/                # 状态管理
│   └── category_provider.dart # 分类状态管理
└── widgets/                  # 可复用组件
```

### 开发流程

1. **安装Flutter依赖**
```bash
cd frontend
flutter pub get
```

2. **配置后端地址**
编辑 `lib/services/api_service.dart`，修改 `baseUrl`：
```dart
static const String baseUrl = 'http://your-backend-address:8000/api/v1';
```

3. **运行应用**
```bash
# 查看可用设备
flutter devices

# 运行应用
flutter run
```

### 添加新页面

1. 在 `lib/screens/` 目录下创建新页面
2. 在 `lib/models/` 中定义数据模型（如需要）
3. 使用 `Navigator.push` 进行页面跳转

示例：
```dart
class NewScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('新页面')),
      body: Center(child: Text('内容')),
    );
  }
}
```

## 数据库设计

### food_category (菜系分类表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | varchar(50) | 分类名称 |
| parent_id | int | 父分类ID |
| keyword | varchar(200) | 检索关键词 |
| icon | varchar(255) | 图标URL |
| sort | int | 排序权重 |
| is_default | tinyint | 是否默认启用 |

### draw_history (抽取历史表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键 |
| user_id | bigint | 用户ID |
| category_id | int | 分类ID |
| category_name | varchar(50) | 分类名称快照 |
| longitude | float | 经度 |
| latitude | float | 纬度 |
| create_time | datetime | 抽取时间 |

### user_category (用户自定义分类表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键 |
| user_id | bigint | 用户ID |
| category_name | varchar(50) | 分类名称 |
| keyword | varchar(200) | 检索关键词 |
| weight | int | 抽取权重 |
| create_time | datetime | 创建时间 |

## API接口文档

### 1. 获取全部分类
```
GET /api/v1/categories

Response:
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": 1,
        "name": "川菜",
        "parent_id": 0,
        "keyword": "川菜,四川菜,麻辣",
        "icon": "chuancai.png",
        "sort": 1,
        "is_default": true
      }
    ]
  }
}
```

### 2. 随机抽取
```
POST /api/v1/draw

Request:
{
  "user_id": 1001,
  "include_custom": true,
  "category_ids": []
}

Response:
{
  "code": 0,
  "data": {
    "draw_id": 98765,
    "category_id": 5,
    "category_name": "泰国菜",
    "icon": "thaifood.png",
    "draw_time": "2026-06-23 12:30:00"
  }
}
```

### 3. 获取商家列表
```
GET /api/v1/merchants/list

Query Parameters:
- category_id: int (必填) - 菜系分类ID
- longitude: float (必填) - 经度
- latitude: float (必填) - 纬度
- sort_type: string - 排序方式 (distance/rating)
- page: int - 页码
- page_size: int - 每页数量
- radius: int - 搜索半径(米)

Response:
{
  "code": 0,
  "data": {
    "total": 45,
    "list": [
      {
        "id": "m001",
        "name": "泰香米泰国餐厅",
        "cover_image": "https://xxx/xxx.jpg",
        "rating": 4.8,
        "review_count": 2356,
        "avg_price": 88,
        "distance": 520,
        "address": "雨花台区应天大街619号",
        "business_status": 1,
        "tags": ["东南亚菜", "冬阴功"]
      }
    ]
  }
}
```

### 4. 获取商家详情
```
GET /api/v1/merchants/{merchant_id}

Response:
{
  "code": 0,
  "data": {
    "id": "m001",
    "name": "泰香米泰国餐厅",
    "cover_image": "https://xxx/xxx.jpg",
    "rating": 4.8,
    "review_count": 2356,
    "avg_price": 88,
    "distance": 520,
    "address": "雨花台区应天大街619号",
    "business_status": 1,
    "tags": ["东南亚菜", "冬阴功"],
    "phone": "025-12345678",
    "business_hours": "10:00-22:00"
  }
}
```

## 常见问题

### 后端
1. **数据库连接失败**
   - 检查 `.env` 文件中的数据库配置
   - 确认MySQL服务已启动
   - 检查数据库用户权限

2. **高德地图API调用失败**
   - 确认已配置有效的 `AMAP_API_KEY`
   - 检查网络连接
   - 查看高德开放平台API调用额度

### 前端
1. **无法连接后端**
   - 检查 `api_service.dart` 中的 `baseUrl` 配置
   - 确认后端服务已启动
   - 检查网络权限和防火墙设置

2. **定位功能异常**
   - 确认已授予应用定位权限
   - 检查设备定位服务是否开启
   - 在Android项目中配置定位权限（AndroidManifest.xml）

## 部署指南

### 后端部署
1. 使用 `gunicorn` 替代 `uvicorn` 用于生产环境
2. 配置Nginx作为反向代理
3. 使用 `systemd` 管理服务
4. 配置SSL证书启用HTTPS

### 前端部署
1. 构建发布版本：`flutter build apk` 或 `flutter build ios`
2. 上传到各应用商店
3. 或构建Web版本：`flutter build web`

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 开启Pull Request
