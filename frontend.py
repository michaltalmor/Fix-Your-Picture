import cv2
import kivy
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivymd.uix.behaviors import HoverBehavior

from yolo_object_detection import Detection

kivy.require('1.9.0')


class FileChoosePopup(Popup):
    load = ObjectProperty()


# creating the root widget used in .kv file
class MyLayout(Widget):
    my_detection = Detection()
    my_image = ObjectProperty(None)
    the_popup = ObjectProperty(None)
    output = ObjectProperty(None)

    def change_picture(self, img_path="party.jpeg"):
        self.my_image.source = img_path

    def detect_objects(self):
        self.my_detection.load_image(self.my_image.source)
        img = self.my_detection.detect_objects()
        grade = self.my_detection.calculate_grade()
        # binding function
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def load_picture(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        new_image_path = str(selection[0])
        self.the_popup.dismiss()
        self.change_picture(new_image_path)


class MyButton(HoverBehavior, Button):
    pass


class MyApp(App):
    def build(self):
        self.title = 'Fix Your Pic'
        return MyLayout()


if __name__ == '__main__':
    Window.borderless = False
    Window.size = (800, 400)
    MyApp().run()
