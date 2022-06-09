#! /usr/bin/python3
from std_msgs.msg import Bool, String,Float32MultiArray
import pynput as pi
import rospy

tecla = String()
rospy.init_node('robot_teleop', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
pubg = rospy.Publisher('/velz',Float32MultiArray, queue_size=1)
Vx = 0
Wz = 0

r=3.3/100
l=26/100
pai=3.1416
Wr = (pai/30)*(Vx/(2*r))
Wl = (pai/30)*(Vx/(2*r))
veloz = Float32MultiArray()
veloz.data = [Wr,Wl]

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
    elif key == pi.keyboard.KeyCode.from_char('e'):
        tecla = "e"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('r'):
        tecla = "r"
        pub.publish(tecla)  
    elif key == pi.keyboard.KeyCode.from_char('f'):
        tecla = "f"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('g'):
        tecla = "g"
        pub.publish(tecla) 
    elif key == pi.keyboard.KeyCode.from_char('t'):
        tecla = "t"
        pub.publish(tecla) 
    elif key == pi.keyboard.KeyCode.from_char('y'):
        tecla = "y"
        pub.publish(tecla) 
    elif key == pi.keyboard.KeyCode.from_char('c'):
        tecla = "c"
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
    elif key == pi.keyboard.KeyCode.from_char('e'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('r'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('f'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('g'):
        tecla = "q"
        pub.publish(tecla)
    elif key == pi.keyboard.KeyCode.from_char('c'):
        tecla = "q"
        pub.publish(tecla)

def main():
    try:
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            connections = pubg.get_num_connections()
            rospy.loginfo('Connections: %d', connections)
            if connections > 0:
                pubg.publish(veloz)
                rospy.loginfo('Published')
                break
            rate.sleep()
    except rospy.ROSInterruptException as e:
        raise e
    with pi.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
