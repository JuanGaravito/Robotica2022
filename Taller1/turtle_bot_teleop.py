#! /usr/bin/python3

import pynput as pi
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

Vx = float(input("Ingrese la velocidad lineal en x \n"))
Wz = float(input("Ingrese la velocidad angular en z \n"))

move_cmd = Twist()
rospy.init_node('turtle_bot_teleop', anonymous=True)
pub = rospy.Publisher('/turtlebot_cmdVel', Twist, queue_size=1)

global Guac;
Guac = []

def callback(msg):
    if msg.data == True:
        guardartxt()

def guardartxt():
 G=[]
 G.append(str(Vx))
 G.append(str(Wz))
 for i in range(len(Guac)):
    G.append(Guac[i])
 LL=input("ingrese el nombre con el que desea guardar el recorrido \n")
 f = open(LL,'a')
 f.write(G[0])
 f.close()
 for i in range(1,len(G)):
    f = open(LL, 'a')
    f.write('\n' + G[i])
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

rospy.Subscriber('/interface_teleop_call',Bool, callback)

def main():
    with pi.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
