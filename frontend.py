import os

import cv2
import kivy
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.image import Image
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
    detect = ObjectProperty(None)

    def change_picture(self, img_path="default.png"):
        self.my_image.source = img_path
        self.my_image.reload()
        if img_path=="default.png":
            self.detect.disabled = True

    def detect_objects(self):
        self.my_detection.load_image(self.my_image.source)
        img = self.my_detection.detect_objects()
        grade = self.my_detection.calculate_grade()
        self.output.text = f"\nYour image grade is: {grade}"
        # binding function
        self.load_detected_image(img)
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def load_detected_image(self, img):
        dot_location = self.my_image.source.rfind('.')
        new_img_path = self.my_image.source[:dot_location] + "2" + self.my_image.source[dot_location:]
        cv2.imwrite(new_img_path, img)
        self.change_picture(new_img_path)


    def load_picture(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        new_image_path = str(selection[0])
        self.the_popup.dismiss()
        self.change_picture(new_image_path)
        self.detect.disabled = False


class MyButton(HoverBehavior, Button):
    pass


class MyApp(App):
    def build(self):
        self.title = 'Fix Your Pic'
        return MyLayout()


if __name__ == '__main__':
    Window.borderless = False
    Window.size = (1000, 500)
    MyApp().run()
