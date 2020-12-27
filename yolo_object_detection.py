import cv2
import numpy as np


class Detection:
    classes = []
    height, width, channels = 0, 0, 0
    img = None
    outs = None
    grade_object = None
    objects_details = None

    def __init__(self):
        # Load Yolo
        self.net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        # load objects names
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        # random colors for objects
        colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def load_image(self, image_path):
        # Loading image
        # img = cv2.imread("bad_grade.jpg")
        self.img = cv2.imread(image_path)
        self.img = cv2.resize(self.img, None, fx=0.2, fy=0.2)
        self.height, self.width, self.channels = self.img.shape

    def detect_objects(self, confidence_level=0.5):
        # Detecting objects
        blob = cv2.dnn.blobFromImage(self.img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Showing informations on the screen
        height, width, channels = self.height, self.width, self.channels
        class_ids = []
        confidences = []
        boxes = []
        # out = layer box with some objects
        for out in outs:
            # detection = single object that was detected
            for detection in out:
                # make sure we dont detect the same object in different outs
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # if confidence > 0.5:
                if confidence > confidence_level:
                    # get object detected details
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    # print(str(self.classes[class_id]))
                    # print(confidences)
        return self.draw_detected_object(confidences, class_ids, boxes)

    def draw_detected_object(self, confidences, class_ids, boxes):
        # grade will calculate like this: 0 - front person, 1 - back person, 2 - other object
        objects_details = []
        grade_object = {
          "f_person": 0,
          "b_person": 0,
          "other_obj": 0
        }
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # print(indexes)
        people = []
        for i in range(len(boxes)):
            if i in indexes:
                # is a person
                if class_ids[i] == 0:
                    people.append(boxes[i])
                    color = [0, 255, 0]
                # is not a person
                else:
                    grade_object["other_obj"] = grade_object["other_obj"] + 1
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = [0, 0, 255]
                    cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(self.img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    # put object index number on pic
                    cv2.putText(self.img, str(len(objects_details)), (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    objects_details.append([label, "other_obj", [x, y, w, h], color])

        if len(people) > 0:
            max_high = np.max(np.array(people)[:, 3])
            # biggest_person = list(filter(lambda x: (np.array(people)[:, 3])[x] == max_high, people))[0]
            threshold_person_size_percent = 0.6
            # front person
            for i in people:
                object_type = ""
                if i[3] == max_high or i[3] >= max_high * threshold_person_size_percent:
                    grade_object["f_person"] = grade_object["f_person"] + 1
                    object_type = "f_person"
                    color = [0, 255, 0]
                # back person
                else:
                    grade_object["b_person"] = grade_object["b_person"] + 1
                    object_type = "b_person"
                    color = [255, 0, 0]
                x, y, w, h = i
                label = str(self.classes[0])
                cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(self.img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                # put object index number on pic
                cv2.putText(self.img, str(len(objects_details)), (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                objects_details.append([label, object_type, [x, y, w, h], color])
        self.grade_object = grade_object
        self.objects_details = objects_details

        ##########################################################################
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ##########################################################################


        return self.img

    def redraw(self, object_index):
        object_type = self.objects_details[object_index][1]
        if object_type == "f_person":
            self.objects_details[object_index][1] = "b_person"
            self.objects_details[object_index][3] = [255, 0, 0]
            self.grade_object["other_obj"] = self.grade_object["other_obj"] + 1
            self.grade_object["f_person"] = self.grade_object["f_person"] - 1
        elif object_type == "b_person" :
            self.objects_details[object_index][1] = "f_person"
            self.objects_details[object_index][3] = [0, 255, 0]
            self.grade_object["f_person"] = self.grade_object["f_person"] + 1
            self.grade_object["b_person"] = self.grade_object["b_person"] - 1
        elif object_type == "other_obj":
            self.objects_details[object_index][1] = "f_person"
            self.objects_details[object_index][3] = [0, 255, 0]
            self.grade_object["f_person"] = self.grade_object["f_person"] + 1
            self.grade_object["other_obj"] = self.grade_object["other_obj"] - 1

        # redraw
        indx = 0
        for i in self.objects_details:
            label = i[0]
            x, y, w, h = i[2]
            color = i[3]

            cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(self.img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # put object index number on pic
            cv2.putText(self.img, str(indx), (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            indx += 1

        return self.img
        ##########################################################################
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ##########################################################################


    def calculate_grade(self):
        grade_object = self.grade_object
        grade = 100
        n_obj = grade_object["other_obj"]
        n_f_person = grade_object["f_person"]
        n_b_person = grade_object["b_person"]
        n = n_obj + n_f_person + n_b_person

        grade = grade - 70*(n_b_person/n) - 30*(n_obj/n)
        return grade

    def get_number_of_objects(self):
        if self.objects_details:
            return len(self.objects_details)



detc = Detection()
# detc.load_image('bad_grade.jpg')
# detc.load_image('woman_in_background.jpg')
detc.load_image('ice_river.jpg')
detc.detect_objects()
print(detc.calculate_grade())

detc.redraw(0)
print(detc.calculate_grade())
detc.redraw(0)
print(detc.calculate_grade())
detc.redraw(0)
print(detc.calculate_grade())
print(detc.get_number_of_objects())

