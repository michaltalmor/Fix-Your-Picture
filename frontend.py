import cv2
import kivy
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.app import App
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
    input = ObjectProperty(None)
    tag = ObjectProperty(None)

    def change_picture(self, img_path="default.png"):
        self.my_image.source = img_path
        self.my_image.reload()
        if img_path == "default.png":
            self.detect.disabled = True
            self.output.text = "\n Load your image to get grade"
            self.input.disabled = True
            self.input.text = ""
            self.tag.disabled = True

    def detect_objects(self):
        self.my_detection.load_image(self.my_image.source)
        img = self.my_detection.detect_objects()
        grade = self.my_detection.calculate_grade()
        self.output.text = f"\nYour image grade is: {grade}"
        # binding function
        self.load_detected_image(img)
        self.input.disabled = False
        self.tag.disabled = False

    def load_detected_image(self, img):
        if self.input.disabled:
            dot_location = self.my_image.source.rfind('.')
            new_img_path = self.my_image.source[:dot_location] + "2" + self.my_image.source[dot_location:]
        else:
            new_img_path = self.my_image.source
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
        self.input.disabled = True
        self.tag.disabled = True
        self.input.text = ""
        self.output.text = "\n Press 'Detect' to get grade"

    def recalculate_and_detect_object(self):
        if not self.input.text.isdigit():
            self.raise_popup("Error", "Input must be a valid integer")
            return None
        index = int(self.input.text)
        if index not in range(self.my_detection.get_number_of_objects()):
            self.raise_popup("Error", "Object index is not exist")
            return None
        img = self.my_detection.redraw(index)
        grade = self.my_detection.calculate_grade()
        self.output.text = f"\nYour image grade is: {grade}"
        self.load_detected_image(img)

    def raise_popup(self, error_type, text, change_size=None):
        content = Button(text=text)
        popup = Popup(title=error_type, content=content, auto_dismiss=False, size_hint=(None, None),
                      size=(450, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()


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
