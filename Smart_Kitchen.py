import RPi.GPIO as GPIO
import time

i=0

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 21
GPIO_ECHO = 20
DBled = 26

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(DBled, GPIO.OUT)

GPIO.setup(16,GPIO.OUT)       #MQ2 Buzzer
GPIO.setup(14,GPIO.IN)		  #MQ@ In 

GPIO.setup(23,GPIO.IN)		 # IR Input	
GPIO.setup(15,GPIO.OUT)			#IR OUT


servo_pin= 12
GPIO.setup(servo_pin,GPIO.OUT)    #Servo motor out
pwm = GPIO.PWM(servo_pin,50)

pwm.start(7)

		# DUST BIN
def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
 
	StartTime = time.time()
	StopTime = time.time()
 
    # save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
 
    # save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
 
    # time difference between start and arrival
	TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2
	
	return distance
	
	

		#GAS DETECTION
def gas():	
	mq= GPIO.input(14)	
	print(mq)
		
	if(mq==1):
		GPIO.output(16, GPIO.HIGH)			#Red LED ON
		print("GAS DETECTED")	
		time.sleep(1)
	
	elif(mq==0):		
		GPIO.output(16, GPIO.LOW)		#Red LED OFF
		print("GAS NOT DETECTED")
		time.sleep(1)

	return gas

		#DOOR
def IR():
		
		global i
		if(GPIO.input(23)==False):		#Object is far away
			GPIO.output(15,True)			#Red LED ON
			print("Door Opened")	
			i=i+1
			
			print('The number of People in the room is',i)			
			time.sleep(0.5)
	
		elif(GPIO.input(23)==True):		#Object is near
			GPIO.output(15,False)		#Red LED OFF
			print("Door Closed")
			time.sleep(0.5)

		#DOOR servo
def door():
	
	
	
	if(GPIO.input(23)==False):
		pwm.ChangeDutyCycle(7.0)
		time.sleep(5)

		pwm.ChangeDutyCycle(2.0)
		#time.sleep()
	
pwm.ChangeDutyCycle(0)


while True:
	
	  
	dist = distance()	
	if dist<10:
		GPIO.output(26, GPIO.HIGH)
	else:
		GPIO.output(26, GPIO.LOW)
		time.sleep(1)    
	
	gas()   	
	IR()
	door()
pwm.stop()
