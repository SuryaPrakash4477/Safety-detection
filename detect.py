from ultralytics import YOLO
import cv2
import cvzone
import math


def safetyDetection(file):
    if file is None : 
        cap = cv2.VideoCapture(0)  # For Webcam
        cap.set(3, 1280)
        cap.set(4, 720)
    else : 
        cap = cv2.VideoCapture(file)  # For Video
    model = YOLO("best.pt")

    Classname = ['Helmet', 'Safety-Vest', 'No-Helmet', 'No-Safety-Vest', 'Person']

    myColor = (0, 0, 255)
    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                w, h = x2 - x1, y2 - y1
                # cvzone.cornerRect(img, (x1, y1, w, h))

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = Classname[cls]
                print(currentClass)
                if conf>0.5:
                    if currentClass =='NO-Helmet' or currentClass =='NO-Safety-Vest':
                        myColor = (0, 0,255) # blue 
                    elif currentClass =='Helmet' or currentClass =='Safety-Vest':
                        myColor =(0,255,0) # green
                    else:
                        myColor = (255, 0, 0) # red 

                    cvzone.putTextRect(img, f'{Classname[cls]} {conf}',
                                    (max(0, x1), max(35, y1)), scale=1, thickness=1,colorB=myColor,
                                    colorT=(255,255,255),colorR=myColor, offset=5)
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    file = None
    safetyDetection(file)
