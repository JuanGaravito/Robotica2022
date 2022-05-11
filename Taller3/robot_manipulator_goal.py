#! /usr/bin/python3

from std_msgs.msg import String,Int16
import rospy
import math as mt
import scipy.optimize as scp
import time as tm
import numpy as np

tecla = String()
rospy.init_node('teleop', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)

brazorad=[2]
brazoang=[90]
def odobrazo1(brazo1):
  brazorad.append(2+2.5*(np.pi/180)*brazo1.data)


#    print(brazorad[-1])

def odobrazo2(brazo2):
     brazoang.append(brazo2.data)

rospy.Subscriber('/Brazolar', Int16, odobrazo1)
rospy.Subscriber('/Brazolado', Int16, odobrazo2)

def poscicion(r,a):
  for i in range(200):
    print(brazorad[-1])
    if (brazorad[-1]<r-0.1):
        tecla = "e"
        pub.publish(tecla)
    elif(brazorad[-1]>r+0.1):
        tecla = "r"
        pub.publish(tecla)
    else:
        tecla = "q"
        pub.publish(tecla)
        break
    tm.sleep(0.1)
  for i in range(10):
       tecla = "q"
       pub.publish(tecla)
  for i in range(200):
      if (brazoang[-1]<a):
        tecla = "f"
        pub.publish(tecla)
      elif(brazoang[-1]>a+0.5):
        tecla = "g"
        pub.publish(tecla)
      else:
        tecla = "q"
        pub.publish(tecla)
        break
      tm.sleep(0.1)
    


               

def main():
    u=float(input("poscicion deseada en X (entre -7,7): "))
    w=float(input("poscicion deseada en Y (entre 2,7):"))
    if u == 0:
      r = w
      a = 90
    else:
      def fun(x):
          a=[x[0]*mt.cos(mt.radians(x[1]))-u,    x[0]*mt.sin(mt.radians(x[1]))-w]
          return a
      sol=scp.fsolve(fun,[0,0])
      r=int(sol[0])
      a=int(sol[1])
    print([r,a])
    poscicion(r,a)



if __name__=='__main__':
    main()