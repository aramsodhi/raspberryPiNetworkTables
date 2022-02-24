import cv2
import numpy as np

import sys
from networktables import NetworkTables


# variables for ball detection:
capture = cv2.VideoCapture(0)

WIDTH = 400
HEIGHT = 300

capture.set(3, WIDTH)
capture.set(4, HEIGHT)

lower = np.array([165, 50, 50]) # lower red
upper = np.array([180, 255, 255]) # upper red

#variables for network tables:
if len(sys.argv) != 2:
    print("Cannot connect to robot")
    exit(0)

ip = sys.argv[1]

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("SmartDashboard")

def send_to_robot(data):
    sd.putNumber("ball_x", data[0])
    sd.putNumber("ball_y", data[1])
    sd.putBoolean("ball_on_screen", data[2])

while True:
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    

    mask = cv2.inRange(hsv, lower, upper)
    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.2, 100)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        circle_x = circles[0][0]
        circle_y = circles[0][1]
        circle_r = circles[0][2]
                               
        cv2.circle(frame, (circle_x, circle_y), circle_r, (0, 255, 0), 4)
        
        justified_x = circle_x - (WIDTH / 2)
        justified_y = (circle_y - (HEIGHT / 2)) * -1
        data = [justified_x, justified_y, True]
        
        print(justified_x, justified_y)
        send_to_robot(data)
    else:
        data = [0, 0, False]
        send_to_robot(data)
        
    cv2.imshow("filtered", blur)
    cv2.imshow("circles", frame)
    
    cv2.waitKey(1)
    
