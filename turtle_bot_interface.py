#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x_vals = []
y_vals = []

def callback(msg):
    x = msg.linear.x
    y = msg.linear.y
    x_vals.append(x)
    y_vals.append(y)
    #print(x_vals)
    #rospy.loginfo('x:{},y:{}'.format(x,y))
fig,ax = plt.subplots()
def animate(i):
    ax.clear()
    ax.set_xlim(-4,4)
    ax.set_ylim(-4,4)
    ax.plot(x_vals,y_vals)

def main():
    rospy.init_node('turtle_bot_interface',anonymous=True)
    rospy.Subscriber('/turtlebot_position', Twist, callback)
    pub = rospy.Publisher('/interface_teleop_call', Bool, queue_size=1)

    ventana = Tk()
    ventana.geometry('642x535')
    ventana.wm_title('Location Monitor')
    ventana.minsize(642,535)

    frame = Frame(ventana)
    frame.pack(expand=1,fill='both')

    def itsclick():
        info = Bool()
        info.data = True
        pub.publish(info)
    
    buttonSave = Button(ventana,text='Guardar Recorrido',command = itsclick)
    buttonSave.pack()

    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.get_tk_widget().pack(expand=1,fill='both')

    toolbar = NavigationToolbar2Tk(canvas,ventana)
    toolbar.update()
    canvas.get_tk_widget().pack(expand=1,fill='both')


    ani = animation.FuncAnimation(fig,animate,interval=500)
    canvas.draw()
    
    plt.title('Location Monitor')
    ventana.mainloop()

if __name__=='__main__':
    main()
    
    









