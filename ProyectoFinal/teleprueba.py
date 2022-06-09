#! /usr/bin/python3
from std_msgs.msg import Int16, String,Float32MultiArray
import pynput as pi
import rospy
import numpy as np
from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from a_star import a_star
from utils import plot_path
import time
tw = 0.35 #15 centimetros
tq = 0.05
tmin = 0.01
tecla = String()
rospy.init_node('robot_teleop', anonymous=False)
pub = rospy.Publisher('/teclas', String, queue_size=1)
pubg = rospy.Publisher('/velz',Float32MultiArray, queue_size=1)
cosenos = []
senos = []
angulos = []

def angulo(data):
    cosenos.append(np.cos(data.data*np.pi/180)) 
    senos.append(np.sin(data.data*np.pi/180))
    angulos.append(data.data)
    print(data.data)

def arribaizquierda():
    print("arribaizquierda")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = 90
    while True:
     if angulos[-1]<88:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]>92:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw)    

def izquierdaabajo():
    print("izquierdaabajo")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = 180
    while True:
     if angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def abajoderecha():
    print("abajoderecha")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = 270
    while True:
     if angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def derechaarriba():
    print("abajoderecha")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = 360
    while True:
     if angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def arribaderecha():
    print("abajoderecha")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = -90
    while True:
     if angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def derechaabajo():
    print("derechaabajo")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = -180
    while True:
     if angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def abajoizquierda():
    print("abajoizquierda")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial = -270
    while True:
     if angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw) 

def izquierdaarriba():
    print("izquierdaarriba")
    pub.publish("q")
    rospy.sleep(tq)
    anguloinicial =-360
    while True:
     if angulos[-1]>anguloinicial+2:
        pub.publish("d")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     elif angulos[-1]<anguloinicial-2:
        pub.publish("a")
        rospy.sleep(tmin)
        pub.publish("q")
        rospy.sleep(tq)
     else:
         break
    pub.publish("q")
    rospy.sleep(tq)
    pub.publish("w")
    rospy.sleep(tw)  

rospy.Subscriber("/angulo",Int16,angulo)

def adelante():
    print("adelante")
    pub.publish("w")
    rospy.sleep(tw)
    pub.publish("q") 

def main():
    try:
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            connections = pubg.get_num_connections()
            rospy.loginfo('Connections: %d', connections)
            if connections > 0:
                rospy.loginfo('Published')
                break
            rate.sleep()
    except rospy.ROSInterruptException as e:
        raise e
    # load the map
    gmap = OccupancyGridMap.from_png('/home/robotica/catkin_robotica/src/mi_robot_8/scripts/grid_mapchiqui.png', 1)

    # set a start and an end node (in meters)
    node0 = (21,1)
    node1 = (4, 3)
    node2 = (4, 6)
    node3 = (4, 10)
    node4 = (36,9)
    node5 = (40,10)
    node6 = (40,6)
    node7 = (40,3)


    goal = input("Escoja una ruta")

    if goal == "1":
        start_node = node0
        goal_node = node1
    elif goal == "2":
        start_node = node0
        goal_node =node2
    elif goal == "3":
        start_node = node0
        goal_node =node3
    elif goal == "4":
        start_node =node1
        goal_node = node4
    elif goal == "5":
        start_node =node2
        goal_node = node4
    elif goal == "6":
        start_node =node3
        goal_node = node4
    elif goal == "7":
        start_node =node4
        goal_node = node5
    elif goal == "8":
        start_node =node4
        goal_node = node6
    elif goal == "9":
        start_node =node4
        goal_node = node7
   
    # run A*
    path, path_px = a_star(start_node, goal_node, gmap, movement='4N')
    print(path)
    gmap.plot()
    plt.yticks(np.arange(13)-0.5)
    plt.xticks(np.arange(44)-0.5)
    from matplotlib.ticker import StrMethodFormatter
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
    plt.grid()

    lista_x = []
    lista_y = []
    for i in path:
        lista_x.append(i[0])
        lista_y.append(i[1])

    delta_x = []
    delta_y = []
    for j in range(len(lista_x)-1):
        delta_x.append(lista_x[j+1] - lista_x[j])
        delta_y.append(lista_y[j+1] - lista_y[j])

    print(delta_x)
    print(delta_y)
    UU=[]

    for i in range(len(delta_x)):
        if delta_x[i] < 0 and delta_y[i] == 0:
            UU.append("Izquierda: ")
            print("Izquierda: ", delta_x[i], delta_y[i])
        elif delta_x[i] > 0 and delta_y[i] == 0:
           UU.append("Derecha: ")
           print("Derecha: ",delta_x[i], delta_y[i])
        elif delta_y[i] < 0 and delta_x[i] == 0:
           UU.append("Pa abajo: ")
           print("Pa abajo: ",delta_x[i], delta_y[i])
        elif delta_y[i] > 0 and delta_x[i] == 0:
           UU.append("Pa arriba: ")
           print("Pa arriba: ",delta_x[i], delta_y[i])
    estadiI= "Pa abajo: "
    for i in range(len(delta_x)):
        if UU[i]=="Izquierda: " and estadiI =="Pa arriba: " :
            arribaizquierda()
            estadiI=UU[i]
        elif UU[i]=="Derecha: " and estadiI =="Pa arriba: " :
            arribaderecha()
            estadiI=UU[i]
        elif UU[i]=="Pa abajo: " and estadiI == "Derecha: " :
            derechaabajo()
            estadiI=UU[i]
        elif UU[i]=="Pa abajo: " and estadiI =="Izquierda: " :
            izquierdaabajo()
            estadiI=UU[i]
        elif UU[i]=="Izquierda: " and estadiI =="Pa abajo: " :
            abajoizquierda()
            estadiI=UU[i]
        elif UU[i]=="Derecha: " and estadiI =="Pa abajo: " :
            abajoderecha()
            estadiI=UU[i]
        elif UU[i]=="Pa arriba: " and estadiI == "Derecha: " :
            derechaarriba()
            estadiI=UU[i]
        elif UU[i]=="Pa arriba: " and estadiI =="Izquierda: " :
            izquierdaarriba()
            estadiI=UU[i]
        else:
            adelante()
            estadiI=UU[i]
    pub.publish("q")

    
    if path:
        # plot resulting path in pixels over the map
        plot_path(path_px)
    else:
        print('Goal is not reachable')

        # plot start and goal points over the map (in pixels)
        start_node_px = gmap.get_index_from_coordinates(start_node[0], start_node[1])
        goal_node_px = gmap.get_index_from_coordinates(goal_node[0], goal_node[1])

        plt.plot(start_node_px[0], start_node_px[1], 'ro')
        plt.plot(goal_node_px[0], goal_node_px[1], 'go')
    plt.show()
    
if __name__ == '__main__':
    main()
