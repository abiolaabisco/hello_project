import RPi.GPIO as GPIO
import time
import smtplib
from datetime import datetime as dt
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from config import LOCATION, RECIPIENT_GROUP, MAIL_SERVER_HOST, MAIL_SERVER_PORT, EMAIL_USER, EMAIL_PSWD

GPIO.setmode(GPIO.BCM)

time.sleep(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def capture_event_callback_5(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH mains Event detected - value: %s' % value)
        #send_mains_on_email()

    else:
        print('LOW mains event detected - value: %s' % value)
        #send_mains_off_email()
def capture_event_callback_6(channel):
    print('event detected on channel:%s' %channel)
    value = GPIO.input(channel)
    
    if value:
        print('HIGH mains Event detected - value: %s' %value)

    else:
        print('LOW mains Event detected -value: %s' %value)
def capture_inverter_event_callback_19(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH inverter Event detected - value: %s' % value)
        #send_inverter_on_email()

    else:
        print('LOW inverter event detected - value: %s' % value)
        #send_inverter_off_email()

def capture_inverter_event_callback_26(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH inverter Event detected - value: %s' % value)
        #send_inverter_on_email()

    else:
        print('LOW inverter event detected - value: %s' % value)
        #send_inverter_off_email()




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
    GPIO.add_event_detect(5, GPIO.BOTH, callback=capture_event_callback_5, bouncetime=200)
   # GPIO.add_event_detect(6, GPIO.BOTH, callback=capture_event_callback_6, bouncetime=200)
   # GPIO.add_event_detect(19, GPIO.BOTH, callback=capture_inverter_event_callback_19, bouncetime=200)
    GPIO.add_event_detect(26, GPIO.BOTH, callback=capture_inverter_event_callback_26, bouncetime=200)
    try:
        while True:
            pass
    except Exception as e:
        print(e)
        GPIO.cleanup()


if __name__ == '__main__':
    main()

