# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:16:20 2019

@author: Kristoffer
"""
#imports necessary for talking to instrument
import minimalmodbus
import serial
#imports necessary for plotting a real-time graph
import datetime as dt
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation




def delay(interval):
    time.sleep(interval/1000)
    
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

have_run=0

if  have_run==0:
    instrument = minimalmodbus.Instrument('COM3', 1)

    instrument.serial.port                     # this is the serial port name
    instrument.serial.baudrate = 9600         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.05          # seconds
    
    instrument.address                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True
    have_run=1
    delay(3000)
    
    #x23323=2

#testreg = instrument.read_float(50, 0x04 ,2,3)  # Registernumber,
#print(testreg)



#arr=[]
#for i in range (0,20):
#    arr.append(instrument.read_float(10, 0x04 ,2,3))


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Read register that will be plotted
    reg10 = instrument.read_float(10, 0x04 ,2,3)
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(reg10)
    
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)
    
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('register 11 over Time')
    plt.ylabel('Pressure (Barg)')

ani=animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000,repeat=1)
plt.show()


# stop command:
# ani.event_source.stop()
