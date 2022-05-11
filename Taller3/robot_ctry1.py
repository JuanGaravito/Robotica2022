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
    
    cv2.imshow('video',frame)
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