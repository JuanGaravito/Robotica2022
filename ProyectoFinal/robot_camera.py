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
   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if color.lower() == "n":
        lower_blue = np.array([0,0,0])
        upper_blue = np.array([255,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

    if color.lower() == "azul":
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([130,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

    if color.lower() == "amarillo":
        lower_yellow = np.array([22, 43, 50], dtype="uint8")
        upper_yellow = np.array([100, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    if color.lower() == "rojo":
        lower_red = np.array([161, 155, 84]) #161,155,84
        upper_red = np.array([179, 255 ,255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('video',result)
    cv2.imshow('mask1',mask)
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