import cv2
import numpy as np

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread("mom_and_me2.jpeg")
img = cv2.resize(img, None, fx=0.2, fy=0.2)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
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
            print(str(classes[class_id]))

print(confidences)
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
            label = str(classes[class_ids[i]])
            color = [0, 0, 255]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
if len(people) > 0:
    max_high = np.max(np.array(people)[:, 3])
    # biggest_person = list(filter(lambda x: (np.array(people)[:, 3])[x] == max_high, people))[0]
    threshold_person_size_percent = 0.6
    for i in people:
        if i[3] == max_high or i[3] >= max_high*threshold_person_size_percent:
            color = [0, 255, 0]
        else:
            color = [255, 0, 0]
        x, y, w, h = i
        label = str(classes[class_ids[0]])
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)


cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("bla bla")
print("michal")
