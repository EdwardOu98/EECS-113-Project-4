#!/usr/bin/python
# Assignment 4 #
# Implemented by: Edward Ou, student ID: 15561434 #

### import Python Modules ###
import threading
import RPi.GPIO as GPIO
import time		# for time delay and threshold

### Pin Numbering Declaration (setup channel mode of the Pi to Board values) ###
GPIO.setwarnings(False)		# to disable warnings
GPIO.setmode(GPIO.BOARD)

### Set GPIO pins (for inputs and outputs) and all setups needed based on assignment description ###
LED_G = 29 # Pin 29 / GPIO 5: Green LED
BTN_G = 22 # Pin 22 / GPIO 25: Green Button
LED_R = 31 # Pin 31 / GPIO 6: Red LED
BTN_R = 12 # Pin 12 / GPIO 18: Red Button
LED_Y = 32 # Pin 32 / GPIO 12: Yellow LED
BTN_Y = 13 # Pin 13 / GOIO 27: Yellow Button
LED_B = 33 # Pin 33 / GPIO 13: Blue LED
BTN_B = 15 # Pin 15 / GPIO 22: Blue Button
Blink_on = False # Blink state, True for blink mode on, False for blink mode off
interval = 1.5 # Blink interval

GPIO.setup(LED_G, GPIO.OUT) # Green LED
GPIO.output(LED_G, False) # Initially turned off
GPIO.setup(BTN_G, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Green Button with initial state low
GPIO.setup(LED_R, GPIO.OUT) # Red LED
GPIO.output(LED_R, False) # Initially turned off
GPIO.setup(BTN_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Red Button with initial state low
GPIO.setup(LED_Y, GPIO.OUT) # Yellow LED
GPIO.output(LED_Y, False) # Initially turned off
GPIO.setup(BTN_Y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Yellow Button with initial state low
GPIO.setup(LED_B, GPIO.OUT) # Blue LED
GPIO.output(LED_B, False) # Initially turned off
GPIO.setup(BTN_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Blue Button with initial state low

# This function detects inputs
def read_pin(pin):
	return GPIO.input(pin)
	
# This function toggles LEDs
def toggle_led(pin):
	GPIO.output(pin, not read_pin(pin))

# This function resets all the LEDs (Trun all of them off)
def reset_led():
	GPIO.output(LED_G, False)
	GPIO.output(LED_R, False)
	GPIO.output(LED_Y, False)
	GPIO.output(LED_B, False)

# This function takes care of blinking and is called by the blinking thread
def blink_thread():
	reset_led()
	s_time = time.time() # Get start time
	while True: # Toggle all LEDs for a given interval
		time.sleep(interval)
		toggle_led(LED_G)
		toggle_led(LED_R)
		toggle_led(LED_Y)
		toggle_led(LED_B)
		# If both the yellow and blue buttons are pressed or it has been in blinking mode
		# for more than 15 seconds, break from the loop
		if(not Blink_on or time.time()-s_time >= 20):
			break
	reset_led()
	print("end of thread")

# This function catches interrupt and spawn the blink_thread() to handle the interrupts
def handle(pin):
	global Blink_on
	if not Blink_on:
		# light corrresponding LED when pushbutton of same color is pressed
		if(pin == BTN_G):
			toggle_led(LED_G)
		if(pin == BTN_R):
			toggle_led(LED_R)
		if(pin == BTN_Y):
			toggle_led(LED_Y)
		if(pin == BTN_B):
			toggle_led(LED_B)
	
		t = None
		# when yellow and blue is pressed simultaneously, enter blink mode
		if(pin == BTN_Y or pin == BTN_B):
			if (not read_pin(BTN_B) and not read_pin(BTN_Y)):
				Blink_on = True
				# print starting thread
				print("starting thread")
				# entering thread
				t = threading.Thread(target=blink_thread)
				t.daemon = True
				t.start()
	else:
		# if in blink mode, use red and green button to control the speed
		# red to slow down (increase interval), green to speed up (decrease interval)
		global interval
		if(pin == BTN_G):
			interval -= 0.25
		elif(pin == BTN_R):
			interval += 0.25
		
		if(pin == BTN_Y or pin == BTN_B):
			if (not read_pin(BTN_B) and not read_pin(BTN_Y)):
				Blink_on = False

### Event listener (Tell GPIO Library to look out for an event on each pushbuttton and pass handle function)
### Function to be run for each push_button detection ###
GPIO.add_event_detect(BTN_G, GPIO.RISING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_R, GPIO.RISING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_Y, GPIO.RISING, callback=handle, bouncetime=200)
GPIO.add_event_detect(BTN_B, GPIO.RISING, callback=handle, bouncetime=200)

# endless loop with delay to wait for event detections
# while True:
#	time.sleep(1e6)
msg = input("Press <Enter> key to exit.\n")		

GPIO.cleanup()
