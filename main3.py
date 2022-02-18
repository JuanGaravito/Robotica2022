#! /usr/bin/python3

import pynput as pi
import rospy
from geometry_msgs.msg import Twist

Vx = float(input("Ingrese la velocidad lineal en x \n"))
Wz = float(input("Ingrese la velocidad angular en z \n"))

move_cmd = Twist()
rospy.init_node('teleop', anonymous=True)
pub = rospy.Publisher('/turtlebot_cmdVel', Twist, queue_size=1)
Guac=[]
def guardartxt(att):
 Guac=[]
 for i in range(len(att)):
    Guac.append(att[i])
    print(Guac)
 LL=input("ingrese el nombre con el que desea guardar el recorrido \n")
 f = open(LL,'a')
 f.write(Guac[0])
 f.close()
 for i in range(1,len(Guac)):
    f = open('posciciontortuga.txt', 'a')
    f.write('\n' +Guac[i])
    f.close()


def on_press(key):
    Guac.append(str(key))
    if key == pi.keyboard.KeyCode.from_char('w'):
        move_cmd.linear.x = Vx
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('s'):
        move_cmd.linear.x = -Vx
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('a'):
        move_cmd.angular.z = Wz
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('d'):
        move_cmd.angular.z = -Wz
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('z'):
        guardartxt(Guac)


def on_release(key):
    if key == pi.keyboard.KeyCode.from_char('w'):
        move_cmd.linear.x = 0
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('s'):
        move_cmd.linear.x = 0
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('a'):
        move_cmd.angular.z = 0
        pub.publish(move_cmd)
    elif key == pi.keyboard.KeyCode.from_char('d'):
        move_cmd.angular.z = 0
        pub.publish(move_cmd)


def main():
    with pi.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
