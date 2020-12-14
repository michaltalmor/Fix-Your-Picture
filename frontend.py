import kivy
from kivy.core.window import Window

kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', False)


# creating the root widget used in .kv file
class Imagekv(BoxLayout):
    '''
        no need to do anything here as
        we are building things in .kv file
    '''
    pass


# class in which name .kv file must be named My.kv.
class MyApp(App):
    def build(self):
        return Imagekv()


if __name__ == '__main__':
    Window.size = (700, 400)
    MyApp().run()
