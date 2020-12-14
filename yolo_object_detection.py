import cv2
import numpy as np


class Detection:
    classes = []
    height, width, channels = 0, 0, 0
    img = None
    outs = None

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
        self.draw_detected_object(confidences, class_ids, boxes)

    def draw_detected_object(self, confidences, class_ids, boxes):
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        people = []
        for i in range(len(boxes)):
            if i in indexes:
                # x, y, w, h = boxes[i]
                # label = str(classes[class_ids[i]])
                # color = colors[class_ids[i]]
                if class_ids[i] == 0:
                    people.append(boxes[i])
                    color = [0, 255, 0]
                else:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = [0, 0, 255]
                    cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(self.img, label, (x, y + 30), font, 3, color, 3)
        if len(people) > 0:
            max_high = np.max(np.array(people)[:, 3])
            # biggest_person = list(filter(lambda x: (np.array(people)[:, 3])[x] == max_high, people))[0]
            threshold_person_size_percent = 0.6
            for i in people:
                if i[3] == max_high or i[3] >= max_high * threshold_person_size_percent:
                    color = [0, 255, 0]
                else:
                    color = [255, 0, 0]
                x, y, w, h = i
                label = str(self.classes[class_ids[0]])
                cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(self.img, label, (x, y + 30), font, 3, color, 3)

        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("bla bla")
        print("michal")


detc = Detection()
detc.load_image('bad_grade.jpg')
detc.detect_objects()


