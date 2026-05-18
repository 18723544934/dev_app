from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import requests
from bs4 import BeautifulSoup

# 窗口设置
Window.size = (450, 700)
# 中文乱码修复
FONT = "C:/Windows/Fonts/msyh.ttc"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


class SearchEngineUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15

        # 默认搜索引擎
        self.current_engine = "baidu"
        self.engine_buttons = {}

        # 标题
        self.add_widget(Label(
            text="多引擎聚合搜索",
            font_size=26, font_name=FONT, bold=True, color=(0.1, 0.3, 0.8, 1)
        ))

        # 搜索引擎切换栏（纯基础Button，无任何新版控件）
        engine_bar = GridLayout(cols=4, size_hint_y=None, height=45, spacing=8)

        # 四个引擎按钮
        btn_baidu = Button(text="百度", font_name=FONT, background_color=(0.2, 0.6, 1, 1))
        btn_bing = Button(text="必应", font_name=FONT)
        btn_quark = Button(text="夸克", font_name=FONT)
        btn_yandex = Button(text="Yandex", font_name=FONT)

        # 绑定点击事件
        btn_baidu.bind(on_press=lambda x: self.change_engine("baidu"))
        btn_bing.bind(on_press=lambda x: self.change_engine("bing"))
        btn_quark.bind(on_press=lambda x: self.change_engine("quark"))
        btn_yandex.bind(on_press=lambda x: self.change_engine("yandex"))

        # 存储按钮
        self.engine_buttons = {
            "baidu": btn_baidu,
            "bing": btn_bing,
            "quark": btn_quark,
            "yandex": btn_yandex
        }

        engine_bar.add_widget(btn_baidu)
        engine_bar.add_widget(btn_bing)
        engine_bar.add_widget(btn_quark)
        engine_bar.add_widget(btn_yandex)
        self.add_widget(engine_bar)

        # 搜索输入框
        self.key_input = TextInput(
            hint_text="输入关键词搜索...",
            font_size=16, font_name=FONT,
            size_hint_y=None, height=55
        )
        self.add_widget(self.key_input)

        # 搜索按钮
        self.search_btn = Button(
            text="立即搜索",
            font_size=17, font_name=FONT,
            background_color=(0.2, 0.7, 0.9, 1),
            size_hint_y=None, height=52
        )
        self.search_btn.bind(on_press=self.start_search)
        self.add_widget(self.search_btn)

        # 状态提示
        self.status = Label(text="就绪", font_name=FONT, font_size=14, color=(0.4, 0.4, 0.4, 1))
        self.add_widget(self.status)

        # 结果滚动区域
        self.scroll = ScrollView()
        self.result_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=6)
        self.result_box.bind(minimum_height=self.result_box.setter("height"))
        self.scroll.add_widget(self.result_box)
        self.add_widget(self.scroll)

    # 切换引擎（单选效果，改变按钮颜色）
    def change_engine(self, engine):
        self.current_engine = engine
        # 重置所有按钮颜色
        for btn in self.engine_buttons.values():
            btn.background_color = (1, 1, 1, 1)
        # 高亮选中的引擎
        self.engine_buttons[engine].background_color = (0.2, 0.6, 1, 1)
        self.status.text = f"已切换：{engine}"
        self.result_box.clear_widgets()

    # 清空结果
    def clear_results(self):
        self.result_box.clear_widgets()

    # 开始搜索
    def start_search(self, instance):
        keyword = self.key_input.text.strip()
        if not keyword:
            self.result_box.add_widget(Label(text="请输入关键词！", font_name=FONT, color=(1, 0, 0, 1)))
            return

        self.clear_results()
        self.status.text = "搜索中..."
        self.search_btn.disabled = True

        try:
            results = []
            if self.current_engine == "baidu":
                results = self.search_baidu(keyword)
            elif self.current_engine == "bing":
                results = self.search_bing(keyword)
            elif self.current_engine == "quark":
                results = self.search_quark(keyword)
            elif self.current_engine == "yandex":
                results = self.search_yandex(keyword)

            self.show_results(results)
            self.status.text = f"完成，共{len(results)}条结果"

        except Exception as e:
            self.result_box.add_widget(Label(text=f"失败：{str(e)}", font_name=FONT, color=(1, 0, 0, 1)))
            self.status.text = "搜索出错"
        finally:
            self.search_btn.disabled = False

    # 百度搜索
    def search_baidu(self, kw):
        resp = requests.get("https://www.baidu.com/s", params={"wd": kw}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return [(i.h3.get_text(strip=True), i.h3.a["href"]) for i in soup.select(".c-container")[:10] if
                i.h3 and i.h3.a]

    # 必应搜索
    def search_bing(self, kw):
        resp = requests.get("https://cn.bing.com/search", params={"q": kw}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return [(i.h2.get_text(strip=True), i.h2.a["href"]) for i in soup.select(".b_algo")[:10] if i.h2 and i.h2.a]

    # 夸克搜索
    def search_quark(self, kw):
        resp = requests.get("https://quark.cn/s", params={"q": kw}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return [(i.get_text(strip=True), i["href"]) for i in soup.select("h3 a")[:10] if i]

    # Yandex搜索
    def search_yandex(self, kw):
        resp = requests.get("https://yandex.com/search", params={"text": kw}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return [(i.get_text(strip=True), i["href"]) for i in soup.select(".serp-item__title")[:10] if i]

    # 展示结果
    def show_results(self, results):
        if not results:
            self.result_box.add_widget(Label(text="未找到结果", font_name=FONT, font_size=16))
            return
        for i, (title, link) in enumerate(results, 1):
            self.result_box.add_widget(
                Label(text=f"{i}. {title}", font_name=FONT, font_size=14, size_hint_y=None, height=40))
            self.result_box.add_widget(
                Label(text=link, font_name=FONT, font_size=11, color=(0, 0, 1, 1), size_hint_y=None, height=25))


class SearchApp(App):
    def build(self):
        self.title = "多引擎搜索"
        return SearchEngineUI()


if __name__ == "__main__":
    SearchApp().run()