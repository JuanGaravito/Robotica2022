#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image

def receive_img(data):
    data.height = 

rospy.Subscriber('usb_cam/image_raw', Image, receive_img)

def main():
    rospy.init_node('resolution_lowerer',anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()