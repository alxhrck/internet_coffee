import wiringpi2 as GPIO
import time

GPIO.wiringPiSetupSys()
PIN = 10
GPIO.pinMode(PIN, 1) # 1 = GPIO.OUT, 0 = GPIO.INPUT
GPIO.digitalWrite(PIN, 1) # 1 = GPIO.HIGH, 0 = GPIO.LOW

try:
	print 'Heating...'
	GPIO.digitalWrite(PIN, 0)
	time.sleep(1)

	print 'Cooling Down...'
	GPIO.digitalWrite(PIN, 1)
	time.sleep(1)
	print 'Enjoy!'

finally:
	#GPIO.digitalWrite(PIN, 0)
	#GPIO.pinMode(PIN, 0) 
	exit()
