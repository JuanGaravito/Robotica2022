#!/usr/bin/env python3
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Int16
color = input("Ingrese el color de la pelota: ")
bridge_obj = CvBridge()
tecla = String()
rospy.init_node('robot_identify_stimate', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
dist = []

def distancia(datos):
    dist.append(datos.data)

def receive_img(data):
    try:
        frame =  bridge_obj.imgmsg_to_cv2(data,desired_encoding='bgr8')  
    except CvBridgeError as e:
        print(e)
   
    x_medium = 0
    y_medium = 0
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    if color.lower()  == "n":
        lower_blue = np.array([0,0,0])
        upper_blue = np.array([255,255,255])
        mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    if color.lower() == "azul":
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([130,255,255])
        mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    if color.lower() == "amarillo":
        lower_yellow = np.array([20, 75, 100], dtype="uint8")
        upper_yellow = np.array([50, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    if color.lower() == "rojo":
        lower_red1 = np.array([0,50,50]) #161,155,84
        upper_red1 = np.array([10,255,255])
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        lower_red2 = np.array([170,50,50]) #161,155,84
        upper_red2 = np.array([180,235,255])
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = mask1 + mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w) / 2)
        y_medium = int((y + y + h) / 2)
        break

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    cv2.line(frame, (0, y_medium), (640, y_medium), (0, 255, 0), 2)

    cv2.line(frame, (320, 0), (320, 480), (0, 120, 0), 2)
    t = 0.1
    if x_medium >= 350:
        print("g")#Rote
        tecla = "g"
        pub.publish(tecla)
        rospy.sleep(t)
        
    if x_medium <= 320:
        #Rote
        print("f")
        tecla = "f"
        pub.publish(tecla)
        rospy.sleep(t)
        
    if x_medium <= 350 and x_medium >= 320:
        #Dejarlo fijo
        print("YAAAAA")
        rospy.sleep(1)
        cv2.destroyAllWindows()
        cv2.line(frame, (320, 0), (320, 480), (255, 255, 255), 2) 
        while dist[-1] > 7:
            print(dist[-1])
            tecla = "e"
            pub.publish(tecla)
            rospy.sleep(t)
            print(tecla)
        for i in range(120):
            tecla = "y"
            pub.publish(tecla)
            print(tecla)
        for i in range(180):
            tecla = "r"
            pub.publish(tecla)
            rospy.sleep(t)
            print(tecla)
        for i in range(15):
            pub.publish("q")
            rospy.sleep(t)
            print(tecla)
        
    cv2.imshow("Frame", frame)
  # cv2.imshow("mask", mask)
    cv2.waitKey(1)

rospy.Subscriber('usb_cam/image_raw', Image, receive_img)
rospy.Subscriber('/distancia', Int16, distancia)

def main():
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()