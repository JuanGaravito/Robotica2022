#! /usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
import tkinter as tk
import time as tm

move_cmd = Twist()
rospy.init_node('teleop', anonymous=True)
pub = rospy.Publisher('/turtlebot_cmdVel', Twist, queue_size=1)
Guac=[]
def Nmoviento(act):
    Vx=float(act[0])
    Wz=float(act[1])
    for i in range(2,len(act)):
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




def main():
    vent=tk.Tk()
    vent.geometry('300x250')
    titu=tk.Label(text="escriba el nombre del archivo txt")
    titu.place(x=50,y=80)
    texc=tk.Entry()
    texc.place(x=70, y=130)
    botnE = tk.Button(text="Recrear recorrido guardado", command=lambda: Recrear(texc.get()))
    botnE.place(x=50, y=170)

    vent.mainloop()




if __name__ == '__main__':
    main()

