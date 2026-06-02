from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# 1080P 手机模拟尺寸
Window.size = (540, 960)
# Windows 中文字体（解决乱码）
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

# -------------------------- 圆角卡片组件（兼容所有Kivy版本） --------------------------
class WhiteCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 220
        self.padding = 25
        self.spacing = 18
        # 白色圆角背景（核心美化）
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[22])
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# -------------------------- 主界面 --------------------------
class TempLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 28
        self.spacing = 28

        # 顶部主题背景（纯色高级蓝，无渐变，兼容旧版）
        with self.canvas.before:
            Color(0.1, 0.5, 0.9, 1)
            self.main_bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[0, 0, 30, 30])
        self.bind(size=self.update_main_bg, pos=self.update_main_bg)

        # 标题（带图标，不用图片也好看）
        self.add_widget(Label(
            text="温度转换器",
            font_size=38,
            bold=True,
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            size_hint_y=None,
            height=90
        ))

        # ========== 摄氏度转换模块 ==========
        self.add_widget(Label(
            text="摄氏度 → 华氏度",
            font_size=22,
            color=(1, 1, 1, 0.95),
            font_name=FONT_PATH
        ))
        # 白色卡片
        c_card = WhiteCard()
        c_card.add_widget(Label(
            text="摄氏度 (℃)",
            font_size=22,
            font_name=FONT_PATH,
            color=(0.2, 0.2, 0.2, 1)
        ))
        # 圆角输入框
        self.c_input = TextInput(
            hint_text="请输入数字",
            font_size=22,
            input_filter="float",
            font_name=FONT_PATH,
            size_hint_y=None,
            height=65,
            background_color=(0.96, 0.98, 1, 1),
            padding=[20, 15],
            cursor_color=(0.1, 0.5, 0.9, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        c_card.add_widget(self.c_input)
        # 蓝色圆角按钮
        self.btn_c2f = Button(
            text="转换为 ℉",
            font_size=22,
            bold=True,
            font_name=FONT_PATH,
            size_hint_y=None,
            height=65,
            background_color=(0.1, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_c2f.bind(on_press=self.c_to_f)
        c_card.add_widget(self.btn_c2f)
        self.add_widget(c_card)

        # ========== 华氏度转换模块 ==========
        self.add_widget(Label(
            text="华氏度 → 摄氏度",
            font_size=22,
            color=(1, 1, 1, 0.95),
            font_name=FONT_PATH
        ))
        # 白色卡片
        f_card = WhiteCard()
        f_card.add_widget(Label(
            text="华氏度 (℉)",
            font_size=22,
            font_name=FONT_PATH,
            color=(0.2, 0.2, 0.2, 1)
        ))
        self.f_input = TextInput(
            hint_text="请输入数字",
            font_size=22,
            input_filter="float",
            font_name=FONT_PATH,
            size_hint_y=None,
            height=65,
            background_color=(0.96, 0.98, 1, 1),
            padding=[20, 15],
            cursor_color=(1, 0.4, 0.2, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        f_card.add_widget(self.f_input)
        # 橙色圆角按钮
        self.btn_f2c = Button(
            text="转换为 ℃",
            font_size=22,
            bold=True,
            font_name=FONT_PATH,
            size_hint_y=None,
            height=65,
            background_color=(1, 0.4, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_f2c.bind(on_press=self.f_to_c)
        f_card.add_widget(self.btn_f2c)
        self.add_widget(f_card)

        # ========== 结果显示（悬浮大字） ==========
        self.result = Label(
            text="转换结果：",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            size_hint_y=None,
            height=90
        )
        self.add_widget(self.result)

    def update_main_bg(self, *args):
        self.main_bg.size = self.size
        self.main_bg.pos = self.pos

    # 转换逻辑
    def c_to_f(self, instance):
        try:
            c = float(self.c_input.text)
            f = c * 9 / 5 + 32
            self.result.text = f"结果：{f:.2f} ℉"
            self.result.color = (0.2, 1, 0.4, 1)
        except:
            self.result.text = "请输入正确数字！"
            self.result.color = (1, 0.2, 0.2, 1)

    def f_to_c(self, instance):
        try:
            f = float(self.f_input.text)
            c = (f - 32) * 5 / 9
            self.result.text = f"结果：{c:.2f} ℃"
            self.result.color = (0.2, 1, 0.4, 1)
        except:
            self.result.text = "请输入正确数字！"
            self.result.color = (1, 0.2, 0.2, 1)

class TempApp(App):
    def build(self):
        self.title = "精致温度转换器"
        return TempLayout()

if __name__ == "__main__":
    TempApp().run()