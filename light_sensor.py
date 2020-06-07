#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from gpiozero import LED

#the distance sensor can measure up to about 4 meters

try:
    #setup:
    
    #GPIO.setmode(BOARD) sets it such as they are using physical pin numbers (1-40)
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER = 7
    PIN_ECHO = 11
    pulse_start_time1 = 0
    pulse_end_time1 = 0
    pulse_start_time2 = 0
    pulse_end_time2 = 0
    light_on = 0; #if light_on = 1, green light is on, if it =0, red light is on
    #sets the trigger pin to be output and echo pin to be input
    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
    
    #LED uses the pins as numbered on the T-Cobbler, also known as BCM numbers
    led_green = LED(6)
    led_red = LED(23)
    
    #set the trigger to low so that it doesn't send any signal until we set it to high.
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    
    print("Wating for sensor to settle")
    
    #use this sleep to ensure sensor gets enough settle time
    time.sleep(2)
    
    print("calculating distance")
    
    while True:
        
        #set amount of measurements pr. second by sleeping in a set time.
        time.sleep(0.25)
        
        #sends out 8-pulse patterns at 40KHz, which will be reffered to as a signal
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        
        #trigger needs a pulse of at least 10 microseconds to start sending a signal.
        #sleep script so that the current lasts long enough so  start the trigger
        time.sleep(0.00001)
        
        #stops sending out a signal
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        
        #checks if ECHO has gotten a response or not (ECHO pin is 1 or 0).
        #ECHO times out after 38 milliseconds, aka gets set to zero again. 
        #uses start and end times to calculate time from when the TRIGGER sent signal to when it was received by ECHO
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time1 = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time1 = time.time()
            
            
        pulse_duration = pulse_end_time1- pulse_start_time1 #time in seconds from TRIGGER sendt signal and ECHO received
        distance = round(pulse_duration * 17150,2) #distance in cm
        print("Distance: " ,distance, " cm")
        
        
        
        #turns on or off lights on conditions
        if(distance<120 and light_on==0):
            light_on+=1
            led_red.off()
            led_green.on()
        elif (distance<120 and light_on==1):
            light_on-=1
            led_green.off()
            led_red.on()
            
        
#end of try statement and ensures pins and such are reset for use in other programs, and turns off lights
finally:
    GPIO.cleanup()
