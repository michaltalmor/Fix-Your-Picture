import kivy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivymd.uix.behaviors import HoverBehavior
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
kivy.require('1.9.0')


# creating the root widget used in .kv file
class MyLayout(Widget):
    def load_picture(self):
        pass


class MyButton(HoverBehavior, Button):
    pass


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    Window.borderless = False
    Window.size = (800, 400)
    MyApp().run()
