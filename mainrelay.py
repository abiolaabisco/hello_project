
import os
import time
import smtplib
from time import strftime
userName= "abiolaabisco37@gmail.com"
password= "adamawaabiola"
mailTo = "abiolaabisco@yahoo.com"
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


print "initialing"

while True:
        power_on = GPIO.input(5)
        power_off = GPIO.input(6)

        power_oninv = GPIO.input(20)
        power_offinv = GPIO.input(21)
        if ((power_on >= 1) & (power_oninv >=1)):
            print 'Main 1 and Main 2 OK'
            detect=strftime("%Y-%n-%d %H-%M-%S")
            msg = MIMEText("main 1 and main 2 ok")
            msg = MIMEText('local deyection time was: ' +detect)
            msg['subject']= 'mains1 and mains2 ok'
            msg['From']=userName
            msg['To']=mailTo

            server=smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo_or_helo_if_needed()
            server.login(userName,password)
            server.sendmail(usr,mailTo, msg.as_string())
            server.quit()
        elif (power_on >= 1):
            print 'Main 2 Not OK'
            detect=strftime("%Y-%n-%d %H-%M-%S")
            msg = MIMEText("main 2 not ok")
            msg = MIMEText('local deyection time was: ' +detect)
            msg['subject']= 'mains 2 not ok'
            msg['From']=userName
            msg['To']=mailTo

            server=smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo_or_helo_if_needed()
            server.login(userName,password)
            server.sendmail(userName,mailTo, msg.as_string())
            server.quit()
        elif (power_oninv >= 1):
            print 'Main 1 Not OK'
            detect=strftime("%Y-%n-%d %H-%M-%S")
            msg = MIMEText("main 1 not ok")
            msg = MIMEText('local deyection time was: ' +detect)
            msg['subject']= 'mains1 not ok'
            msg['From']=userName
            msg['To']=mailTo

            server=smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo_or_helo_if_needed()
            server.login(userName,password)
            server.sendmail(userName,mailTo, msg.as_string())
            server.quit()
            
        if ((power_on >= 1) | (power_oninv >=1)):
            
            print "POWER"
            detect=strftime("%Y-%n-%d %H-%M-%S")
            msg = MIMEText("power")
            msg = MIMEText('local deyection time was: ' +detect)
            msg['subject']= 'power'
            msg['From']=userName
            msg['To']=mailTo

            server=smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo_or_helo_if_needed()
            server.login(userName,password)
            server.sendmail(userName,mailTo, msg.as_string())
            server.quit()
            if (power_on >= 1):
                print "Main 1"
                detect=strftime("%Y-%n-%d %H-%M-%S")
                msg = MIMEText("main 1")
                msg = MIMEText('local deyection time was: ' +detect)
                msg['subject']= 'mains 1'
                msg['From']=userName
                msg['To']=mailTo

                server=smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo_or_helo_if_needed()
                server.login(userName,password)
                server.sendmail(userName,mailTo, msg.as_string())
                server.quit()
            else:
                print "Main 2 -- Power One is down running on Inverter"
                detect=strftime("%Y-%n-%d %H-%M-%S")
                msg = MIMEText("Main 2 -- Power One is down running on Inverter")
                msg = MIMEText('local deyection time was: ' +detect)
                msg['subject']= 'Main 2 -- Power One is down running on Inverter'
                msg['From']=userName
                msg['To']=mailTo

                server=smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo_or_helo_if_needed()
                server.login(userName,password)
                server.sendmail(userName,mailTo, msg.as_string())
                server.quit()
           # time.sleep(10)
        elif ((power_off >= 1) | (power_offinv >=1)):
                print "POWER OFF"
                detect=strftime("%Y-%n-%d %H-%M-%S")
##                msg = MIMEText("POWER OFF")
##                msg = MIMEText('local deyection time was: ' +detect)
##                msg['subject']= 'POWER OFF'
##                msg['From']=userName
##                msg['To']=mailTo
##
##                server=smtplib.SMTP('smtp.gmail.com:587')
##                server.ehlo_or_helo_if_needed()
##                server.login(userName,password)
##                server.sendmail(userName,mailTo, msg.as_string())
##                server.quit()
                if (power_off >= 1):
                    print "Main 1 and Main 2 - Off"
##                    detect=strftime("%Y-%n-%d %H-%M-%S")
##                    msg = MIMEText("main 1 and main 2 ok")
##                    msg = MIMEText('local deyection time was: ' +detect)
##                    msg['subject']= 'mains1 and mains2 off'
##                    msg['From']=userName
##                    msg['To']=mailTo
##
##                    server=smtplib.SMTP('smtp.gmail.com:587')
##                    server.ehlo_or_helo_if_needed()
##                    #server.login(userName,password)
##                    server.sendmail(userName,mailTo, msg.as_string())
##                    server.quit()
                else:
                    print "Main 2 Off"
                    
##                    detect=strftime("%Y-%n-%d %H-%M-%S")
##                    msg = MIMEText("main 1 and main 2 ok")
##                    msg = MIMEText('local deyection time was: ' +detect)
##                    msg['subject']= 'mains2 off'
##                    msg['From']=userName
##                    msg['To']=mailTo
##
##                    server=smtplib.SMTP('smtp.gmail.com:587')
##                    server.ehlo_or_helo_if_needed()
##                    server.login(userName,password)
##                    server.sendmail(userName,mailTo, msg.as_string())
##                    server.quit()
                time.sleep(2)
##        except KeyboardInterrupt:
##                GPIO.cleanup()
##                print "quit"
time.sleep(1)
GPIO.cleanup()

