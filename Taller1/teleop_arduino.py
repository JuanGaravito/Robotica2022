#! /usr/bin/python3

import pynput as pi
import rospy
from std_msgs.msg import String

Vx = float(input("Ingrese la velocidad lineal en x \n"))
Wz = float(input("Ingrese la velocidad angular en z \n"))

tecla = String()
rospy.init_node('turtle_bot_teleop', anonymous=True)
pub = rospy.Publisher('/teclas', String, queue_size=1)

def on_press(key):
    if key == pi.keyboard.KeyCode.from_char('w'):
        tecla = "w"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('s'):
        tecla = "s"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('a'):
        tecla = "a"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('d'):
        tecla = "d"
        pub.publish(tecla)  

def on_release(key):
    if key == pi.keyboard.KeyCode.from_char('w'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('s'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('a'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('d'):
        tecla = "q"
        pub.publish(tecla)


def main():
    with pi.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
