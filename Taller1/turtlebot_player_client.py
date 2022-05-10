#! /usr/bin/python3
import rospy
from geometry_msgs.msg import Twist

from prueba23std_msgs.srv import *
import tkinter as tk
import time as tm
import sys as ss

Vx=50
Wz=50

move_cmd = Twist()
rospy.init_node('teleop', anonymous=True)
pub = rospy.Publisher('/turtlebot_cmdVel', Twist, queue_size=1)
Guac=[]

def Nmoviento(act):
    for i in range(len(act)):
        key=act[i]
        if key == 'w':
            move_cmd.linear.x = Vx
            pub.publish(move_cmd)
        elif key == 's':
            move_cmd.linear.x = -Vx
            pub.publish(move_cmd)
        elif key == 'a':
            move_cmd.angular.z = Wz
            pub.publish(move_cmd)
        elif key == 'd':
            move_cmd.angular.z = -Wz
            pub.publish(move_cmd)
        elif key == 'z':
            move_cmd.linear.x = 0
            move_cmd.angular.z = 0
            pub.publish(move_cmd)
        tm.sleep(0.03)
    print("recorrido terminado")


def Recrear(nom):
    f = open(nom, 'r')
    HH = f.read()
    RR = list(HH)
    RR1 = list(filter(lambda a: a != "'", RR))
    RH2 = list(filter(lambda a: a != "\n", RR1))
    f.close()
    print(RH2)
    Nmoviento(RH2)

def numfun(name):
    rospy.wait_for_service('filename')
    try:
        aaa=rospy.ServiceProxy('filename',nameFile)
        res=aaa(name)
        Recrear(str(res.name))
        return res.name
    except rospy.ServiceException as e:
        print("el servicio fallo")





if __name__ == '__main__':

    if len(ss.argv)==2:
        name=str(ss.argv[1])
        print(name)
    else:
        print("esta")
        ss.exit()
    numfun(name)

