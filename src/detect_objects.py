from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import time
import math
import threading
from datetime import date
from data import write_data, write_cars, read_data
from tests.speed_test import new_csv, speed_check

test = False

adress = 'videos/traffic1.3gpp'
adress2 = 'videos/traffic-stock.mp4'

# time check for amount of traffic
time_check = 60

# time for refreshing image for API
time_refresh = 10

cars = 0

def get_live_image(path):
    image = cv2.imread(path)
    return image

def get_video():
    dataset = read_data(file='input.json')
    adress = dataset['path']
    capture = cv2.VideoCapture(adress)
    return capture

def save_API_image(image=None):
    if image==None:
        return
    threading.Timer(20.0, save_API_image).start()
    image.save(f'static/live.jpg') 

def detect_objects():

    # Read video
    cap = get_video()

    # read CNN
    model = YOLO("yolov8n.pt")

    i = 0
    avg = 0
    counter = 0
    start_time = time.time()
    not_avg = True
    new_csv(test)
    # main loop

    while True:
        ret, img= cap.read()
        results = model.predict(img, stream=False)
        counter+=1
        for result in results:
 
            cars = 0

            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                speed_check(result, test)
                if class_id == 'car' or class_id == 'truck' or class_id == 'bus':
                    cars+=1

                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = round(box.conf[0].item(), 2)

                    image1 = Image.fromarray(result.plot()[...,::-1])

            i+=1

            if i % 5 == 0:
                image1.save(f'static/detection.jpg')
                write_cars(cars, file="data.json")

                live_image = Image.fromarray(np.uint8(img))
                save_API_image(live_image)
                i=0

        print("Cars on the frame : ", cars)
        avg+=cars
        # Getting the average, reset the timer
        if time.time() - start_time >= time_check:
            curr_avg = math.ceil(avg/counter)
            print("Average amount of a cars per minute: ", curr_avg)
            write_data(cars, curr_avg)
            avg = 0
            counter = 0
            start_time = time.time()
            not_avg = False
        elif not_avg:
            write_data(cars, "In progress...")

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
  detect_objects()
