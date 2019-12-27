import time
import RPi.GPIO as GPIO
import smtplib
import os

GPIO.setmode (GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

print ("initializing")

while True:
    power_on = GPIO.input(5)
    power_off = GPIO.input(6)

    power_oninver =GPIO.input(21)
    power_offinver =GPIO.input(19)
    if ((power_on >=1)& (power_oninver>=1)):
        print ('main 1 and main 2 is ok')

    elif (power_on>=1):
        print('mains 2 not ok')

    elif (power_offinver>=1):
        print('mains  1 not ok')
        
    if ((power_on >=1)|(power_oninver>=1)):
        print('power')
        if (power_on>=1):
            print('mains 1')

        else:
            print('mains 2')

    elif ((power_off>=1)|(power_offinver>=1)):
        print ('power off')
        if (power_off >=1):
            print('mains 1 and mains 2 off')
        else:
            print ('mains 2 off')
            time.sleep(2)
#       except KeyboardInterrupt:
#          GPIO.cleanup()
            
time.sleep(1)
GPIO.cleanup()
