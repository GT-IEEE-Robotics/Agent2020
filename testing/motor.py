import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

controlpin = [11,13,15,16]

for pin in controlpin:
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,0)

seq = [[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]]

for i in range(512):
	for halfstep in range(8):
		print(seq[halfstep])
		for pin in range(4):
			GPIO.output(controlpin[pin], seq[halfstep][pin])
		time.sleep(.001)

GPIO.cleanup()
