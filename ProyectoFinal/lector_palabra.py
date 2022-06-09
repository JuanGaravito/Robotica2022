#!/usr/bin/env python3
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Int16
from pytesseract import pytesseract

bridge_obj = CvBridge()
tecla = String()
rospy.init_node('robot_identify_stimate', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
dist = []

def distancia(datos):
    dist.append(datos.data)

contador = []
contador.append(0)
print(contador)
def receive_img(data):
    try:
        frame =  bridge_obj.imgmsg_to_cv2(data,desired_encoding='bgr8')  
        
    except CvBridgeError as e:
        print(e)

    if contador[-1] == 0:        
        img_sin_norm = cv2.imwrite('/home/robotica/catkin_robotica/src/mi_robot_8/scripts/saquese.jpg', frame)
        contador.append(1)
        a.unregister()
        img_sin_norm = cv2.imread('/home/robotica/catkin_robotica/src/mi_robot_8/scripts/saquese.jpg')

        norm_img = np.zeros((img_sin_norm.shape[0], img_sin_norm.shape[1]))
        img_final = cv2.normalize(img_sin_norm, norm_img, 0, 255, cv2.NORM_MINMAX)
        img_final = cv2.threshold(img_final, 100, 220, cv2.THRESH_BINARY)[1]
        img_final = cv2.GaussianBlur(img_final, (1, 1), 0)
        cv2.imwrite("Gauss.jpg", img_final)

        img_gris = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("Cropped.jpg", img_gris)
        path_to_tesseract = r"/home/robotica/.local/lib/python3.8/site-packages/pytesseract.exe"
        text1 = pytesseract.image_to_string(img_gris)
        print("gris: ", text1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
a  = rospy.Subscriber('usb_cam/image_raw', Image, receive_img)
rospy.Subscriber('/distancia', Int16, distancia)

def main():
    try:
        rospy.spin()
        print("esta")
        img_sin_norm = cv2.imread('/home/robotica/catkin_robotica/src/mi_robot_8/scripts/saquese.jpg')

        norm_img = np.zeros((img_sin_norm.shape[0], img_sin_norm.shape[1]))
        img_final = cv2.normalize(img_sin_norm, norm_img, 0, 255, cv2.NORM_MINMAX)
        img_final = cv2.threshold(img_final, 100, 220, cv2.THRESH_BINARY)[1]
        img_final = cv2.GaussianBlur(img_final, (1, 1), 0)
        cv2.imwrite("Gauss.jpg", img_final)

        img_gris = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("Cropped.jpg", img_gris)
        path_to_tesseract = r"/home/robotica/.local/lib/python3.8/site-packages/pytesseract.exe"
        text1 = pytesseract.image_to_string(img_gris)
        print("gris: ", text1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()