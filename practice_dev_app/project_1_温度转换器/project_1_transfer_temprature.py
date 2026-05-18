from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# 设置窗口大小（电脑端预览）
Window.size = (350, 450)

# 【关键】指定中文字体路径（Windows系统自带）
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑，大部分Windows都有

class TempLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 垂直排列
        self.orientation = "vertical"
        self.padding = 30
        self.spacing = 15

        # 标题（指定中文字体）
        self.add_widget(Label(text="温度转换器", font_size=25, bold=True, font_name=FONT_PATH))

        # 输入摄氏度（指定中文字体）
        self.c_label = Label(text="输入摄氏度(℃)：", font_size=16, font_name=FONT_PATH)
        self.add_widget(self.c_label)
        self.c_input = TextInput(hint_text="请输入数字", font_size=18, input_filter="float", font_name=FONT_PATH)
        self.add_widget(self.c_input)

        # 摄氏转华氏按钮（指定中文字体）
        self.btn_c2f = Button(text="转为华氏度(℉)", font_size=16, background_color=(0.2,0.6,1,1), font_name=FONT_PATH)
        self.btn_c2f.bind(on_press=self.c_to_f)
        self.add_widget(self.btn_c2f)

        # 输入华氏度（指定中文字体）
        self.f_label = Label(text="输入华氏度(℉)：", font_size=16, font_name=FONT_PATH)
        self.add_widget(self.f_label)
        self.f_input = TextInput(hint_text="请输入数字", font_size=18, input_filter="float", font_name=FONT_PATH)
        self.add_widget(self.f_input)

        # 华氏转摄氏按钮（指定中文字体）
        self.btn_f2c = Button(text="转为摄氏度(℃)", font_size=16, background_color=(1,0.5,0.2,1), font_name=FONT_PATH)
        self.btn_f2c.bind(on_press=self.f_to_c)
        self.add_widget(self.btn_f2c)

        # 结果显示（指定中文字体）
        self.result = Label(text="转换结果：", font_size=18, color=(1,1,1,1), font_name=FONT_PATH)
        self.add_widget(self.result)

    # 摄氏度 → 华氏度
    def c_to_f(self, instance):
        try:
            c = float(self.c_input.text)
            f = c * 9 / 5 + 32
            self.result.text = f"转换结果：{f:.2f} ℉"
        except:
            self.result.text = "请输入正确数字！"

    # 华氏度 → 摄氏度
    def f_to_c(self, instance):
        try:
            f = float(self.f_input.text)
            c = (f - 32) * 5 / 9
            self.result.text = f"转换结果：{c:.2f} ℃"
        except:
            self.result.text = "请输入正确数字！"

class TempApp(App):
    def build(self):
        self.title = "简易温度转换"
        return TempLayout()

if __name__ == "__main__":
    TempApp().run()