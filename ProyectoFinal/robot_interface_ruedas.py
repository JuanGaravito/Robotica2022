#!/usr/bin/env python3
import numpy as np
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String
from tkinter import *
from matplotlib.figure import Figure
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

def apenea(tecla):
    Guac.append(tecla.data)

def odometriapos(velocidades):
    phir = np.around(velocidades.data[0],2)
    phil = np.around(velocidades.data[1],2)
    if phir != 0.0 or phil != 0.0:
        print(phir,phil)
    Vd = r*phir
    Vi = r*phil
    dt = 20e-3
    posicionesX.append(posicionesX[-1] + 0.5*(Vd+Vi) * np.cos(theta[-1]) * dt)
    posicionesY.append(posicionesY[-1] + 0.5*(Vd + Vi) * np.sin(theta[-1]) * dt)
    theta.append(theta[-1] - (1 / l) * (Vd - Vi) * 2*dt) 
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
rospy.Subscriber('/velocidades', Float32MultiArray, odometriapos)
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
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    diffXmY = len(posicionesX) - len(posicionesY)
    print(diffXmY)
    if diffXmY == 0:
        ax.plot(posicionesX,posicionesY)
    elif diffXmY < 0:
        #for i in range(abs(diffXmY)):
        posicionesX.extend(0*list(range(diffXmY)))
    else:
        #for i in range(abs(diffXmY)):
        posicionesY.extend(0*list(range(diffXmY)))
        
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

    ani = animation.FuncAnimation(fig,animate,interval=50,blit=True)
    canvas.draw()

    plt.title('Location Monitor')
    ventana.mainloop()

    #resultado = MessageBox.askquestion("Guardar", 
    #"¿Quiere guardar el recorrido de su robot?")  
    #if resultado == "no":
    #    buttonSave["state"] = DISABLED

if __name__=='__main__':
    main()
    