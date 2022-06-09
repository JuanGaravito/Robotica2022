#!/usr/bin/env python3

from xxlimited import Xxo
import numpy as np
import rospy
from std_msgs.msg import Int16, Float32MultiArray
from std_msgs.msg import String
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import messagebox as MessageBox

posicionesX=[0]
posicionesY=[0]
theta =[np.pi/2]

global Guac;
Guac = []

r=3.3/100
l=26/100
Vx = 0
Wz = 0
velocidadizquierda = 0
velocidadderecha = 0
velsizqs = []
velsders = []

def apenea(tecla):
    datat = tecla.data
    Guac.append(datat)

def velocidadizq(vel):
    velocidadizquierda = vel.data
    velsizqs.append(velocidadizquierda)
    #print("viene de izquierda",len(velsizqs),len(velsders))
    if len(velsizqs)==len(velsders):
        velocidades = [velsders[-1],velsizqs[-1]]
        odometriapos(velocidades)

def velocidadder(vel):
    velocidadderecha = vel.data
    velsders.append(velocidadderecha)
    #print("viene de derecha",len(velsizqs),len(velsders))
    if len(velsizqs)==len(velsders):
        velocidades = [velsders[-1],velsizqs[-1]]
        odometriapos(velocidades)

def odometriapos(velocidades):
    phir = velocidades[0]
    phil = velocidades[1]
    #if phir != 0.0 or phil != 0.0:
        #print(phir,phil)
    Vd = r*phir
    Vi = r*phil
    dt = 20e-3
    posicionesX.append(posicionesX[-1] + 0.5*(Vd+Vi) * np.cos(theta[-1]) * dt)
    posicionesY.append(posicionesY[-1] + 0.5*(Vd + Vi) * np.sin(theta[-1]) * dt)
    theta.append(theta[-1] - (1 / l) * (Vd - Vi) * 2.1*dt)
    print(theta[-1]*180/np.pi) 

brazorad=[1]
brazoang=[90]
def odobrazo1(brazo1):
    if(brazorad[-1]<15 and brazorad[-1]>0 ):
     if(brazo1.data==90):
        brazorad.append(brazorad[-1])
     elif(brazo1.data==0):
       brazorad.append(brazorad[-1]+0.8)
     elif(brazo1.data==180):
       brazorad.append(brazorad[-1]-0.8)
    elif(brazorad[-1]>=15):
         brazorad.append(14.9)
    elif(brazorad[-1]<=0):
         brazorad.append(0.1)
    #print(brazorad[-1])

def odobrazo2(brazo2):
    if(brazo2.data==90):
        brazoang.append(brazoang[-1])
    elif(brazo2.data==0):
       brazoang.append(brazoang[-1]-5)
    elif(brazo2.data==180):
     brazoang.append(brazoang[-1]+5)

################################
    # if -100>phir:
    #     phir = -100
    # elif phir>100:
    #     phir = 100
    # elif -100>phil:
    #     phil = -100
    # elif phil>100:
    #     phil = 100
        
    # if -100<phir<100 and -100<phil<100:

    #     Vd = r*phir
    #     Vi = r*phil
    #     dt = 0.001
    #     posicionesX.append(posicionesX[-1] + 0.5*(Vd+Vi) * np.cos(theta[-1]) * dt)
    #     posicionesY.append(posicionesY[-1] + 0.5*(Vd + Vi) * np.sin(theta[-1]) * dt)
    #     theta.append(theta[-1] + (1 / l) * (Vd - Vi) * dt)
        #print(posicionesX[-1],posicionesY[-1])
#################################

def guardaVelz(velz):
    Vx = velz.data[0]
    Wz = velz.data[1]

rospy.init_node('robot_interface',anonymous=False)
rospy.Subscriber('/velocidadizq', Int16, velocidadizq)
rospy.Subscriber('/velocidadder', Int16, velocidadder)
rospy.Subscriber('/Brazolar', Int16, odobrazo1)
rospy.Subscriber('/Brazolado', Int16, odobrazo2)
rospy.Subscriber('/teclas', String, apenea)
rospy.Subscriber('/velz',Float32MultiArray,guardaVelz)

def guardartxt():
    G = []
    for i in range(len(Guac)):
        G.append(Guac[i])
    LL = input("ingrese el nombre con el que desea guardar el recorrido \n")
    f = open(LL,'a')
    f.write(str(Vx)+","+str(Wz)+",")
    f.close()
    for i in range(1,len(G)):
        f = open(LL, 'a')
        f.write('\n' + G[i])
        f.close()

fig,ax = plt.subplots()
def animate(i):
    ax.clear()
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_xticks(range(-3,3))
    ax.set_yticks(range(-3,3))
    ax.grid()
    XX=brazorad[-1]*np.cos((np.pi/180)*brazoang[-1])
    YY=brazorad[-1]*np.sin((np.pi/180)*brazoang[-1])
    #print(XX,YY)
    try:
        UU=[]
        WW=[]
        #print(len(brazoang))
        #print(len(brazorad))
        for i in range(len(brazoang)):
           UU.append(brazorad[i]*np.cos((np.pi/180)*brazoang[i]))
           WW.append(brazorad[i]*np.sin((np.pi/180)*brazoang[i]))


   
        ax.scatter(posicionesX[-1],posicionesY[-1],c="red")
        ax.plot(np.array(posicionesX),np.array(posicionesY))
        #ax.scatter(XX,YY,c="red")
        #ax.plot(UU,WW)
    except:
        ax.scatter(posicionesX[-1],posicionesY[-1],c="red")
        #ax.scatter(XX,YY,c="red")
        
def main():
    ventana = Tk()
    ventana.geometry('642x535')
    ventana.wm_title('Location Monitor')
    ventana.minsize(642,535)

    frame = Frame(ventana)
    frame.pack(expand=1,fill='both')

    buttonSave = Button(ventana,text='Guardar Recorrido',command = guardartxt)
    buttonSave.pack()
    Button(ventana, text="Quit", command=ventana.destroy).pack() 

    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.get_tk_widget().pack(expand=1,fill='both')

    toolbar = NavigationToolbar2Tk(canvas,ventana)
    toolbar.update()
    canvas.get_tk_widget().pack(expand=1,fill='both')

    ani = animation.FuncAnimation(fig,animate,interval=50)
    canvas.draw()

    plt.title('Location Monitor')
    ventana.mainloop()

    #resultado = MessageBox.askquestion("Guardar", 
    #"¿Quiere guardar el recorrido de su robot?")  
    #if resultado == "no":
    #    buttonSave["state"] = DISABLED

if __name__=='__main__':
    main()
    