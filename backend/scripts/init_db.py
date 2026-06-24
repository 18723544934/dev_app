import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import FoodCategory
from app.config import settings

# 预置菜系分类数据
CATEGORIES_DATA = [
    # 中式菜系
    (1, "川菜", 0, "川菜,四川菜,麻辣,麻辣香锅", "chuancai.png", 1, True),
    (2, "粤菜", 0, "粤菜,广东菜,早茶,点心", "yuecai.png", 2, True),
    (3, "湘菜", 0, "湘菜,湖南菜,剁椒,臭豆腐", "xiangcai.png", 3, True),
    (4, "鲁菜", 0, "鲁菜,山东菜,海鲜", "lucai.png", 4, True),
    (5, "江浙菜", 0, "江浙菜,苏菜,浙菜,淮扬菜", "jiangzhecai.png", 5, True),
    (6, "东北菜", 0, "东北菜,东北炖菜,锅包肉", "dongbei.png", 6, True),
    (7, "西北菜", 0, "西北菜,新疆菜,羊肉串", "xibei.png", 7, True),
    (8, "云南菜", 0, "云南菜,过桥米线,汽锅鸡", "yunnan.png", 8, True),
    (9, "贵州菜", 0, "贵州菜,酸汤鱼,折耳根", "guizhou.png", 9, True),
    (10, "客家菜", 0, "客家菜,梅菜扣肉,盐焗鸡", "kejia.png", 10, True),
    (11, "潮汕菜", 0, "潮汕菜,潮汕牛肉火锅", "chaoshan.png", 11, True),
    (12, "北京菜", 0, "北京菜,烤鸭,炸酱面", "beijing.png", 12, True),
    (13, "安徽菜", 0, "安徽菜,徽菜,臭鳜鱼", "anhui.png", 13, True),

    # 异国料理
    (14, "日料/寿司", 0, "日料,寿司,日本料理,刺身,拉面", "japanese.png", 14, True),
    (15, "韩式料理", 0, "韩式料理,韩国料理,韩式烤肉,炸鸡", "korean.png", 15, True),
    (16, "泰国菜", 0, "泰国菜,泰餐,冬阴功,芒果糯米饭", "thai.png", 16, True),
    (17, "越南菜", 0, "越南菜,越南粉,春卷", "vietnamese.png", 17, True),
    (18, "印度菜", 0, "印度菜,咖喱,印度飞饼", "indian.png", 18, True),
    (19, "西餐/牛排", 0, "西餐,牛排,意面,沙拉", "western.png", 19, True),
    (20, "意大利菜", 0, "意大利菜,披萨,意面,意大利面", "italian.png", 20, True),
    (21, "法式料理", 0, "法式料理,法餐,法式甜点", "french.png", 21, True),
    (22, "墨西哥菜", 0, "墨西哥菜,塔可,墨西哥卷", "mexican.png", 22, True),
    (23, "东南亚菜", 0, "东南亚菜,新加坡菜,马来西亚菜", "southeast_asian.png", 23, True),
    (24, "中东料理", 0, "中东料理,土耳其菜,烤肉", "middle_eastern.png", 24, True),

    # 火锅烧烤
    (25, "川渝火锅", 0, "川渝火锅,重庆火锅,四川火锅", "chongqing_hotpot.png", 25, True),
    (26, "潮汕牛肉火锅", 0, "潮汕牛肉火锅,牛肉火锅", "chaoshan_hotpot.png", 26, True),
    (27, "猪肚鸡火锅", 0, "猪肚鸡火锅,猪肚鸡", "zhuduji.png", 27, True),
    (28, "椰子鸡火锅", 0, "椰子鸡火锅,椰子鸡", "coconut_chicken.png", 28, True),
    (29, "韩式烤肉", 0, "韩式烤肉,韩式烤肉店", "korean_bbq.png", 29, True),
    (30, "中式烧烤", 0, "中式烧烤,烧烤,撸串", "chinese_bbq.png", 30, True),
    (31, "日式烧肉", 0, "日式烧肉,日式烤肉", "japanese_bbq.png", 31, True),
    (32, "铁板烧", 0, "铁板烧,铁板", "teppanyaki.png", 32, True),

    # 面食小吃
    (33, "兰州拉面", 0, "兰州拉面,拉面,牛肉面", "lanzhou_noodle.png", 33, True),
    (34, "重庆小面", 0, "重庆小面,小面,重庆面条", "chongqing_noodle.png", 34, True),
    (35, "螺蛳粉", 0, "螺蛳粉,螺狮粉", "luosifen.png", 35, True),
    (36, "桂林米粉", 0, "桂林米粉,米粉", "guilin_noodle.png", 36, True),
    (37, "沙县小吃", 0, "沙县小吃,拌面,扁肉", "shaxian.png", 37, True),
    (38, "陕西面食", 0, "陕西面食,肉夹馍,凉皮,biangbiang面", "shanxi_noodle.png", 38, True),
    (39, "生煎/锅贴", 0, "生煎,锅贴,煎包", "shengjian.png", 39, True),
    (40, "饺子馆", 0, "饺子馆,饺子,水饺", "dumpling.png", 40, True),
    (41, "粥铺", 0, "粥铺,粥,早餐粥", "porridge.png", 41, True),

    # 快餐简餐
    (42, "汉堡炸鸡", 0, "汉堡,炸鸡,肯德基,麦当劳", "burger.png", 42, True),
    (43, "中式快餐", 0, "中式快餐,盖饭,快餐", "chinese_fastfood.png", 43, True),
    (44, "盖浇饭", 0, "盖浇饭,盖饭,盖浇", "gaifan.png", 44, True),
    (45, "便当", 0, "便当,盒饭,外卖便当", "bento.png", 45, True),
    (46, "三明治", 0, "三明治,三文治,汉堡", "sandwich.png", 46, True),
    (47, "沙拉轻食", 0, "沙拉,轻食,减脂餐", "salad.png", 47, True),
    (48, "披萨", 0, "披萨,意大利披萨", "pizza.png", 48, True),

    # 特色品类
    (49, "小龙虾", 0, "小龙虾,麻辣小龙虾,十三香小龙虾", "crayfish.png", 49, True),
    (50, "烤鱼", 0, "烤鱼,万州烤鱼", "grilled_fish.png", 50, True),
    (51, "牛蛙", 0, "牛蛙,烤牛蛙,剁椒牛蛙", "bullfrog.png", 51, True),
    (52, "串串香", 0, "串串香,串串", "chuanxiang.png", 52, True),
    (53, "麻辣烫", 0, "麻辣烫,麻辣烫店", "malatang.png", 53, True),
    (54, "冒菜", 0, "冒菜,冒菜店", "maocai.png", 54, True),
    (55, "香锅", 0, "香锅,干锅,干锅店", "xiangguo.png", 55, True),
    (56, "打边炉", 0, "打边炉,广东火锅", "dabianlu.png", 56, True),
    (57, "早茶点心", 0, "早茶,点心,广式点心", "dimsum.png", 57, True),
]


def init_categories():
    """初始化菜系分类数据"""
    db: Session = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(FoodCategory).count()
        if existing_count > 0:
            print(f"数据库中已存在 {existing_count} 条分类数据，跳过初始化")
            return

        # 批量插入数据
        categories = []
        for cat_data in CATEGORIES_DATA:
            category = FoodCategory(
                id=cat_data[0],
                name=cat_data[1],
                parent_id=cat_data[2],
                keyword=cat_data[3],
                icon=cat_data[4],
                sort=cat_data[5],
                is_default=cat_data[6]
            )
            categories.append(category)

        db.bulk_save_objects(categories)
        db.commit()

        print(f"成功初始化 {len(categories)} 条菜系分类数据")

    except Exception as e:
        db.rollback()
        print(f"初始化失败: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("开始初始化数据库...")
    print(f"数据库连接: {settings.DATABASE_URL}")

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

    # 初始化分类数据
    init_categories()

    print("数据库初始化完成！")
