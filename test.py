# This script to used to remotely control the software H11890ver200
# The operations include HV ON, Start, Stop, HV OFF, Save
# Used for Walle 4.0
# Please install following lib to run the script properly
# yiiin33333@gmail.com


import uiautomation as auto
import os
import sys
import threading
import time
import subprocess

run = input( "Start? > " )
secs = 0
timer0 = eval(input( "After how many seconds you want to start the software?" ))
timer1 = eval(input( "How many seconds you want to record?" ))
question3 = eval(input( "What game time do you want? please enter 'number'" ))
question4 = eval(input( "What file name do you want?" ))
def startTimer():
    print("start timer now\n")
if run == "start":
    timer = threading.Timer(1.0, startTimer)
    timer.start()
    
time.sleep(timer0)
print(auto.GetRootControl())
subprocess.Popen( 'H11890ver0200.exe')
H11890Window = auto.WindowControl(searchDepth=1, ClassName='TForm1')
print(H11890Window.Name)
H11890Window.SetTopmost(True)

# after the software is started, search device first
bu0=H11890Window.ButtonControl(searchDepth=2, foundIndex=1)
time.sleep(1)
print(bu0.Name)
bu0.Click()
print("Searching device")

gate1=auto.EditControl(searchDepth=3, foundIndex=4)
gate1.Click()
gate1.Click()
# change the number here to change the gate time
gate1.SendKeys(question3)


bu1=H11890Window.ButtonControl(searchDepth=2, foundIndex=6)
# The unit is sec
# This timer here is when to actually 'START' the software
time.sleep(1)                              
print(bu1.Name)
bu1.Click()
print(" HV ON button was clicked ")

bu2=H11890Window.ButtonControl(searchDepth=2, foundIndex=4)
time.sleep(1)
print(bu2.Name)
bu2.Click()
print(" Start button was clicked ")

# This timer is used to 'STOP' the recording
# Enter the num of secs user wants to use the software
bu3=H11890Window.ButtonControl(searchDepth=2, foundIndex=3)
time.sleep(timer1)
print(bu3.Name)
bu3.Click()
print(" Stop button was clicked ")

bu4=H11890Window.ButtonControl(searchDepth=2, foundIndex=5)
time.sleep(1)
print(bu4.Name)
bu4.Click()
print(" HV OFF button was clicked ")

bu5=H11890Window.ButtonControl(searchDepth=2, foundIndex=2)
time.sleep(1)
print(bu5.Name)
bu5.Click()
print(" Saved  Button is Clicked ")
bu5.SendKeys(question4)
bu6 = auto.WindowControl(searchDeapth=1,ClassName = '#32770')
print(bu6.Name)
bu6.SendKeys('{ENTER}')
print(" File is saved")
#print ( "close the software" )

