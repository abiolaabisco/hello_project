import RPi.GPIO as GPIO
import time
import smtplib
from datetime import datetime as dt

GPIO.setmode(GPIO.BCM)

time.sleep(5)

GPIO.setmode(GPIO.BCM)
#GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def capture_event_callback(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH mains Event detected - value: %s' % value)
        send_mains_on_email()
        push_to_elastic(channel,value,time.ctime())
    else:
        print('LOW mains event detected - value: %s' % value)
        send_mains_off_email()
        push_to_elastic(channel,value,time.ctime())


def capture_inverter_event_callback(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH inverter Event detected - value: %s' % value)
        send_inverter_on_email()

    else:
        print('LOW inverter event detected - value: %s' % value)
        send_inverter_off_email()


def push_to_elastic(channel,value, event_time):
    print('Send Event to ES - %s' % channel)


def send_mains_on_email():
    pass


def send_mains_off_email():
    pass


def send_inverter_on_email():
    pass


def send_inverter_off_email():
    pass


def main():
 #   GPIO.add_event_detect(5, GPIO.BOTH, callback=capture_event_callback, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=capture_event_callback, bouncetime=200)
#    GPIO.add_event_detect(20, GPIO.BOTH, callback=capture_inverter_event_callback, bouncetime=200)
    GPIO.add_event_detect(21, GPIO.BOTH, callback=capture_inverter_event_callback, bouncetime=200)



    while True:
        #    print("Waiting to detect event")
        time.sleep(50000)


if __name__ == '__main__':
    main()

