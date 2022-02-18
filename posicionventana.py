#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
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
    


def main():
    rospy.init_node('location_monitor',anonymous=True)
    rospy.Subscriber('/turtlebot_position', Twist, callback)
    
fig,ax = plt.subplots()
plt.title('Location Monitor')


def animate(i):
    ax.clear()
    ax.set_xlim(-4,4)
    ax.set_ylim(-4,4)
    ax.plot(x_vals,y_vals)

ventana = Tk()
ventana.geometry('642x535')
ventana.wm_title('Location Monitor')
ventana.minsize(642,535)

frame = Frame(ventana)
frame.pack(expand=1,fill='both')

canvas = FigureCanvasTkAgg(fig,master=frame)
canvas.get_tk_widget().pack(expand=1,fill='both')

toolbar = NavigationToolbar2Tk(canvas,ventana)
toolbar.update()
canvas.get_tk_widget().pack(expand=1,fill='both')


ani = animation.FuncAnimation(fig,animate,interval=1000)
canvas.draw()

if __name__=='__main__':
    main()
    ventana.mainloop()
    









