#! /usr/bin/python3
from ast import Global
from cmath import e
from contextlib import ContextDecorator
import rospy
from std_msgs.msg import String

from mi_robot_8.srv import *
from mi_robot_8.srv import robot_player
import tkinter as tk
import time as tm
import sys as ss

tecla = String()
rospy.init_node('teleop', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
global Guac;
Guac=[]

def Nmoviento(act):
        for i in range(len(act)):
            print(act[i])
            if act[i]=="w":
                Guac.append("w")
                tecla = "w"
                pub.publish(tecla)
            elif act[i]=="s":
                Guac.append("s")
                tecla = "s"
                pub.publish(tecla)
            elif act[i]=="a":
                Guac.append("a")
                tecla = "a"
                pub.publish(tecla)
            elif act[i]=="d":
                Guac.append("d")
                tecla = "d"
                pub.publish(tecla)   
            elif act[i]=="q":
                Guac.append("q")
                tecla = "q"
                pub.publish(tecla) 
            tm.sleep(0.02)
        for i in range(100):
            tecla = "q"
            pub.publish(tecla) 
        print("recorrido terminado")


def Recrear(nom):
    f = open(nom, 'r')
    HH = f.read()
    RR = list(HH)
    RR1 = list(filter(lambda a: a != "'", RR))
    RH2 = list(filter(lambda a: a != "\n", RR1))
    c = 0;
    Vs = []
    posprimeracoma = 0;
    for i in range(len(RH2)):
        if RH2[i] == "," and c == 0:
            c += 1
            posprimeracoma = i
        elif RH2[i] == "," and c == 1:
            c += 1
        else:
            Vs.append(RH2[i])
            print(Vs)
        if c == 2:
            break
    global Vx,Wz
    Vx = float("".join(Vs[0:posprimeracoma]))
    Wz = float("".join(Vs[posprimeracoma:len(Vs)]))
    f.close()
    Nmoviento(RH2)

def numfun(name):
    rospy.wait_for_service('filename')
    try:
        aaa=rospy.ServiceProxy('filename',robot_player)
        res=aaa(name)
        Recrear(str(res.name))
        return res.name
    except rospy.ServiceException as e:
        print("el servicio fallo")

if __name__ == '__main__':
    print(ss.argv)
    if len(ss.argv)==2:
        name=str(ss.argv[1])
        print(name)
    else:
        print("esta")
        ss.exit()
    numfun(name)