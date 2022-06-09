#!/usr/bin/env python3
import rospy
from mi_robot_8.srv import robot_player,robot_playerResponse

def handel_name(req):
    print("RETURNUNG"+" "+req.file)
    return robot_playerResponse(req.file)
def addfileServer():
    rospy.init_node("filename_server")
    s=rospy.Service('filename',robot_player,handel_name)
    print("name")
    rospy.spin()
if __name__ == '__main__':
    addfileServer()
