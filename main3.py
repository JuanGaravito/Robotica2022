#! /usr/bin/python3
import rospy
from prueba23std_msgs.srv import nameFile,nameFileResponse

def handel_name(req):
    print("RETURNUNG"+" "+req.file)
    return nameFileResponse(req.file)
def addfileServer():
    rospy.init_node("filename_server")
    s=rospy.Service('filename',nameFile,handel_name)
    print("name")
    rospy.spin()
if __name__ == '__main__':
    addfileServer()
