#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Int16

rospy.init_node('robot_identify_stimate', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
dist = []

def distancia(datos):
    dist.append(datos.data)
    print(dist[-1])


rospy.Subscriber('/distancia', Int16, distancia)
t = 0.1

def main():
    try:
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            connections = pub.get_num_connections()
            rospy.loginfo('Connections: %d', connections)
            
            if connections > 0:
                for i in range(10):
                    tecla = "t"
                    pub.publish(tecla)
                    rospy.sleep(t)
                    print(tecla)
                while dist[-1] >= 10:
                    tecla = "e"
                    pub.publish(tecla)
                    rospy.sleep(t)
                    print(tecla)
                for i in range(10):
                    tecla = "y"
                    pub.publish(tecla)
                    rospy.sleep(t)
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
                    
                rospy.loginfo('Published')
                break
            rate.sleep()
    except rospy.ROSInterruptException as e:
        raise e 

if __name__ == '__main__':
    main()

