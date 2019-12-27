import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()

time.sleep(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(6,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

print "Initialization"

def capture_event_callback(channel):
    print('event detected on channel: %s'% channel)
    value = GPIO.input(channel)
    if value:
        print('HIGH Event detected - value: %s' %value)
    else:
        print('LOW event detected - value: %s' %value) 
    
def capture_falling_callback(channel):
    print('Falling Event detected on channel: %s'%channel)
    

GPIO.add_event_detect(5, GPIO.BOTH, callback=capture_event_callback)
GPIO.add_event_detect(6, GPIO.BOTH, callback=capture_event_callback)

#GPIO.add_event_detect(6, GPIO.RISING, callback=capture_rising_callback)
#GPIO.add_event_detect(6, GPIO.FALLING, callback=capture_falling_callback)

#GPIO.add_event_detect(20, GPIO.BOTH, callback=capture_event_callback)
#GPIO.add_event_detect(21, GPIO.BOTH, callback=capture_event_callback)


while True:
#    print("Waiting to detect event")
    time.sleep(50000)
    

    

