import os
import time
import smtplib
from time import strftime
from email.mime.text import MIMEText
from datetime import datetime as dt
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from confiig import LOCATION, RECIPIENT_GROUP, MAIL_SERVER_HOST, MAIL_SERVER_PORT, EMAIL_USER, EMAIL_PSWD
from Queue import Queue
from threading import Thread
import RPi.GPIO as GPIO
from elasticsearch import Elasticsearch 
import json

es = Elasticsearch('http://10.60.17.131:9200')
power_index='power_mon_data'



GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)



power_on = GPIO.input(5)
power_off = GPIO.input(6)

power_oninv = GPIO.input(20)
power_offinv = GPIO.input(21)

prev_mains_off_val = power_off
prev_inv_off_val = power_offinv
prev_mains_on_val = power_on
prev_inv_on_val = power_oninv

def process_event(j):
    while True:
        val = j.get()
        print(val)
        if (val['pin'] == 5):
            send_mains_on_email(val['time'])
            push_to_elastic(es, power_index,{'location' : 'minna', 'event': 'mains_on', 'time' :val['time']} )
        elif (val['pin'] == 6):
            send_mains_off_email(val['time'])
            push_to_elastic(es, power_index,{'location' : 'minna', 'event':'mains_off', 'time' : val['time']}) 
                
        elif (val['pin'] == 20):
            send_inverter_on_email(val['time'])
            push_to_elastic(es, power_index,{'location' :'minna', 'event': 'inverter_on', 'time' : val['time']}) 
                
        elif(val['pin'] == 21):
            send_inverter_off_email(val['time'])
            push_to_elastic(es, power_index,{'location' : 'minna', 'event': 'inverter_off', 'time' : val['time']}) 

            
        j.task_done()
       
def push_to_elastic(endPoint, index, data):
    endPoint.index(index=index, doc_type='doc', body=json.loads(json.dumps(data)))
    
def send_mains_on_email(event_time):
    subject = "Mains is On @ "+ LOCATION
    body = """
            Mains On at {location}.
            **************************
            MAINS is On
            **************************
            Event Time: {event_time}
            
            """.format(location=LOCATION, event_time=event_time)
    send_mail(subject, body)

def send_mains_off_email(event_time):
    subject = "Mains is down @ " + LOCATION
    body = """
            Mains Down at {location}.
            **************************
            MAINS is Down
            **************************
            Event Time: {event_time}

            """.format(location=LOCATION, event_time=event_time)
    send_mail(subject, body)

def send_inverter_on_email(event_time):
    subject = "Inverter is On @ " + LOCATION
    body = """
            Inverter On at {location}.
            **************************
            INVERTER is On
            **************************
            Event Time: {event_time}

            """.format(location=LOCATION, event_time=event_time)
    send_mail(subject, body)

def send_inverter_off_email(event_time):
    subject = "Inverter is Down @ " + LOCATION
    body = """
            Inverter Down at {location}.
            **************************
            INVERTER is Down
            **************************
            Event Time: {event_time}

            """.format(location=LOCATION, event_time=event_time)
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

print "initialing"
time.sleep(4)

print GPIO.input(20)
q=Queue(maxsize=0)
worker = Thread(target=process_event, args=(q,))
worker.setDaemon(True)
worker.start()

while True:
        power_on = GPIO.input(5)
        power_off = GPIO.input(6)

        power_oninv = GPIO.input(20)
        power_offinv = GPIO.input(21)

        if((prev_mains_on_val != power_on) & (power_on >= 1)):
            print("Mains on")
            prev_mains_on_val = power_on
            prev_mains_off_val = power_off
            event =  {'pin' : 5, 'time': time.strftime("%c")}
            q.put(event)
        elif((prev_mains_off_val != power_off) & (power_off >= 1)):
            print("Mains off")
            prev_mains_off_val = power_off
            prev_mains_on_val = power_on
            event =  {'pin' : 6, 'time': time.strftime("%c")}
            q.put(event)
        elif((prev_inv_on_val != power_oninv) & (power_oninv >= 1)):
            print("Inverter on")
            prev_inv_on_val = power_oninv
            prev_inv_off_val = power_offinv
            event =  {'pin' : 20, 'time': time.strftime("%c")}
            q.put(event)
        elif((prev_inv_off_val != power_offinv) & (power_offinv >= 1)):
            print("Inverter off")
            prev_inv_off_val = power_offinv
            prev_inv_on_val = power_oninv
            event =  {'pin' : 21, 'time': time.strftime("%c")}
            q.put(event)


        time.sleep(5)


        # if ((power_on >= 1) & (power_oninv >=1)):
        #     print 'Main 1 and Main 2 OK'
        #     send_mains_on_email()
        #     send_inverter_on_email()
        # elif (power_on >= 1):
        #     print 'Main 2 Not OK'
        #     send_inverter_off_email()
        # elif (power_oninv >= 1):
        #     print 'Main 1 Not OK'
        #     send_mains_off_email()
        #
        #
        # if ((power_on >= 1) | (power_oninv >=1)):
        #     print "POWER"
        #
        #     if (power_on >= 1):
        #         print "Main 1"
        #         send_mains_on_email()
        #     else:
        #         print "Main 2 -- Power One is down running on Inverter"
        #         send_mains_off_email()
        #         send_inverter_on_email()
        #     time.sleep(10)
        # elif ((power_off >= 1) | (power_offinv >=1)):
        #         print "POWER OFF"
        #         if (power_off >= 1):
        #             print "Main 1  - Off"
        #             send_mains_off_email()
        #         else:
        #             print "Main 2 Off"
        #             send_inverter_off_email()
        #         time.sleep(2)
##        except KeyboardInterrupt:
##                GPIO.cleanup()
##                print "quit"
time.sleep(1)
GPIO.cleanup()
