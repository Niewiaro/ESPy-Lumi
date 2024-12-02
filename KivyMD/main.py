from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon

class ESPy_LumiApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        label = MDLabel(text="Hello, World!", halign="center", font_style="Display")
        # label.font_size = "32sp"
        return label


if __name__ == "__main__":
    ESPy_LumiApp().run()