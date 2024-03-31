from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon

class ESPy_LumiApp(MDApp):
    def build(self):
        label = MDLabel(text="Hello, World!", halign="center", font_style='H1')
        return label


if __name__ == "__main__":
    ESPy_LumiApp().run()