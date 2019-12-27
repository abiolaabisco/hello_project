import os
import time
import smtplib
from time import strftime
from email.mime.text import MIMEText
from datetime import datetime as dt
from email import Encoders
from email.MIMEText import MIMEText

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

power_on = GPIO.input(5)
power_off = GPIO.input(6)

power_oninv = GPIO.input(20)
power_offinv = GPIO.input(21)
print "initialing"
 

##while True:
##    power_on = GPIO.input(5)
##    power_off = GPIO.input(6)
##
##    power_oninv = GPIO.input(20)
##    power_offinv = GPIO.input(21)
def captured_mains(channel):
    print 'event detected on channel:%s' %channel
    value = GPIO.input(channel)
    if ((power_on >= 1) & (power_oninv >=1)):
        print 'Main 1 and Main 2 OK'

    elif (power_on >= 1):
        print 'Main 2 Not OK'
        print 'main 1 ok'
def captured_inverter(channel):
    print 'event detected on channel:%s' %channel
    value = GPIO.input(channel)
    if (power_oninv >= 1):
        print 'Main 1 Not OK'
        print 'main 2 ok'

def captured_power(channel):
    print 'event detected on channel:%s' %channel
    value = GPIO.input(channel)
    if ((power_on >= 1) | (power_oninv >=1)):
        print "POWER on both inverter and mains"

        if (power_on >= 1):
            print "Main 1"
                

        else:
            print "Main 2 -- Power One is down running on Inverter"

            time.sleep(10)
    elif ((power_off >= 1) | (power_offinv >=1)):
        
        print "POWER OFF"

        if (power_off >= 1):
            print "Main 1 and Main 2 - Off"

        else:
            
            print "Main 2 Off"
                    

            time.sleep(2)

def send_mains_on_email():
    subject = "Mains is On @ "+ LOCATION
    body = """
            Mains On at {location}.
            **************************
            MAINS is On
            **************************
            Event Time: {event_time}""".format(location=LOCATION, event_time=time.strftime("%c"))
    send_mail(subject, body)


def send_mains_off_email():
    subject = "Mains is down @ " + LOCATION 
    body = """
            Mains Down at {location}.
            **************************
            MAINS is Down
            **************************
            Event Time: {event_time}""".format(location=LOCATION, event_time=time.strftime("%c"))
    send_mail(subject, body)


def send_inverter_on_email():
    subject = "Inverter is On @ " + LOCATION 
    body = """
            Inverter On at {location}.
            **************************
            INVERTER is On
            **************************
            Event Time: {event_time}""".format(location=LOCATION, event_time=time.strftime("%c"))
    send_mail(subject, body)


def send_inverter_off_email():
    subject = "Inverter is Down @ " + LOCATION 
    body = """
            Inverter Down at {location}.
            **************************
            INVERTER is Down
            **************************
            Event Time: {event_time}""".format(location=LOCATION, event_time=time.strftime("%c"))
    send_mail(subject, body)


def send_mail(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT_GROUP
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    mailServer = smtplib.SMTP(MAIL_SERVER_HOST, MAIL_SERVER_PORT)
    mailServer.starttls()
    mailServer.login(EMAIL_USER, EMAIL_PSWD)
    mailServer.sendmail(EMAIL_USER, RECIPIENT_GROUP, msg.as_string())
    mailServer.quit()


def main():
    GPIO.add_event_detect(5, GPIO.BOTH, callback=captured_mains, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=captured_mains, bouncetime=200)
    GPIO.add_event_detect(20, GPIO.BOTH, callback=captured_inverter, bouncetime=200)
    GPIO.add_event_detect(21, GPIO.BOTH, callback=captured_inverter, bouncetime=200)
    try:
        while True:
            pass
    except Exception as e:
        print(e)
        GPIO.cleanup()


if __name__ == '__main__':
    main()

    

            

time.sleep(1)
GPIO.cleanup()

