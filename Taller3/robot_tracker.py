#!/usr/bin/env python3
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

color = input("Ingrese el color de la pelota: ")
bridge_obj = CvBridge()

def receive_img(data):
    try:
        frame =  bridge_obj.imgmsg_to_cv2(data,desired_encoding='bgr8')  
    except CvBridgeError as e:
        print(e)

    x_medium = 0
    y_medium = 0

    low_red = np.array([90,50,50])
    high_red = np.array([130,255,255])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w) / 2)
        y_medium = int((y + y + h) / 2)
        break

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    cv2.line(frame, (0, y_medium), (640, y_medium), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("mask", red_mask)
    cv2.waitKey(1)

rospy.Subscriber('usb_cam/image_raw', Image, receive_img)

def main():
    rospy.init_node('robot_camera',anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()
