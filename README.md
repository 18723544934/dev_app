# 今天吃啥

一款解决用户 "选择困难症" 的餐饮决策工具，通过随机抽取菜系分类的方式帮用户快速决定用餐方向，并基于地理位置推荐周边对应品类的商家。

## 项目结构

```
do_you_eat/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── models.py     # 数据库模型
│   │   ├── schemas.py    # Pydantic模型
│   │   ├── config.py     # 配置管理
│   │   └── database.py   # 数据库连接
│   ├── scripts/          # 初始化脚本
│   ├── main.py          # 应用入口
│   └── requirements.txt  # Python依赖
└── frontend/             # 前端应用
    ├── lib/
    │   ├── models/      # 数据模型
    │   ├── screens/     # 页面
    │   ├── services/    # API服务
    │   └── providers/   # 状态管理
    └── pubspec.yaml     # Flutter依赖
```

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: MySQL + Redis
- **地图服务**: 高德地图开放平台
- **API文档**: 自动生成 (Swagger UI)

### 前端
- **框架**: Flutter
- **状态管理**: Provider
- **定位**: Geolocator
- **动画**: flutter_animate

## 快速开始

### 后端启动

1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和高德地图API Key
```

3. 创建数据库
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE do_you_eat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. 初始化数据库
```bash
python scripts/init_db.py
```

5. 启动服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看API文档

### 前端启动

1. 安装Flutter SDK
```bash
# 请参考 https://docs.flutter.dev/get-started/install
```

2. 安装依赖
```bash
cd frontend
flutter pub get
```

3. 配置后端地址
编辑 `lib/services/api_service.dart`，修改 `baseUrl` 为你的后端地址

4. 运行应用
```bash
flutter run
```

## 功能特性

### 核心功能
- ✅ 随机抽取菜系分类
- ✅ 基于LBS定位推荐周边商家
- ✅ 距离/评分多维度排序
- ✅ 抽取历史记录
- ✅ 全部分类浏览与筛选

### 菜系分类
- 中式菜系: 川菜、粤菜、湘菜、鲁菜等
- 异国料理: 日料、韩式、泰国菜、西餐等
- 火锅烧烤: 川渝火锅、韩式烤肉、中式烧烤等
- 面食小吃: 兰州拉面、螺蛳粉、沙县小吃等
- 快餐简餐: 汉堡炸鸡、中式快餐、沙拉轻食等
- 特色品类: 小龙虾、烤鱼、串串香、麻辣烫等

## API文档

### 获取全部分类
```
GET /api/v1/categories
```

### 随机抽取
```
POST /api/v1/draw
Body: {
  "user_id": 1001,
  "include_custom": true,
  "category_ids": []
}
```

### 获取商家列表
```
GET /api/v1/merchants/list
Query: category_id, longitude, latitude, sort_type, page, page_size, radius
```

## 配置说明

### 高德地图API Key
1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册账号并创建应用
3. 获取Web服务API Key
4. 在后端 `.env` 文件中配置 `AMAP_API_KEY`

### 数据库配置
在 `.env` 文件中配置MySQL连接信息：
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=do_you_eat
```

## 开发计划

- [ ] 用户自定义分类
- [ ] 分类权重设置
- [ ] 商家收藏功能
- [ ] 评价与评论
- [ ] 社交分享
- [ ] 多城市支持

## 许可证

MIT License
