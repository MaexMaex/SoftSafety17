#!/usr/bin/python

# Software Safety
# Assignment 1.2
# Gantry Controller
# Benjamin Bergens, Niklas Simons, Marcus Norrgard

import sys
import argparse
import random
import time

# Gantry controller
def main(x_next):
	# Magnet starts as released
	gantryLoaded = False
	print "#### GANTRY OPERATION TERMINAL 1.0 ####"
	x_next = int(x_next)
	simulateMove(2)
	print "Object at position x: " + str(x_next)
	x_now = startMotor(gantryLoaded)
	print "Gantry at postition x: " + str(x_now)
	#checking the x_values
	inputSanityCheck(x_next)
	sensorSanityCheck(x_now)
	simulateMove(2)
	print "Scheaduling pickup!" 
	simulateMove(2)
	(x_now, gantryLoaded) = move(x_next, x_now, gantryLoaded)
	simulateMove(2)
	print "Taking object to loading bay"
	returnToLoadingBay(x_now, gantryLoaded)

def inputSanityCheck(x_next):
	if x_next > 10 or x_next < 0:
		panicHaltGracefully("Opertor placed object out of bounds, halting!!!")
def sensorSanityCheck(x_now):
	if x_now > 10:
		panicHaltGracefully("S_X sensor saturated. Halting!!!")

def startMotor(gantryLoaded):
	start = random.randint(0,3)
	if start==3:
		panicHaltGracefully("Engine failed to start!!!")
	print "starting engines..."
	return s_x("start","")

# Method triggers the gantry to move back to the loading bay
# Also checks with s_left that we dont go too far
def returnToLoadingBay(x_now, gantryLoaded):
	counter=0
	x_start=x_now
	bay = s_left(x_now)
	while bay!=True:
		if counter >= 3:
			panicHalt(gantryLoaded,"s_x did not recover within three times, I will halt!!!")
		x_now = motorL(x_now)
		#checking the result of the motors revolution, has s_x failed
		if x_now==x_start:
			print "s_x failed"
			counter=counter+1
		if x_now < x_start:
			x_start=x_now
			counter=0
		# Check with s_left sensor where we are after each move
		bay = s_left(x_now)
	toggleMagnet(gantryLoaded)
#check with s_right that we aren't trying to go over x0
def checkS_right(x_now, gantryLoaded):
	end = s_right(x_now)
	if end:
		panicHalt(gantryLoaded, "Input wants me to go on, but I have reached the end of the boom, I will halt.")

# Movement controller, handels the motors and the magnet
def move(x_next, x_now, gantryLoaded):
	print "Gantry moving"
	#initialize all pointers
	x_start=x_now
	counter=0
	while gantryLoaded == False:
		if x_next > x_now:
			#check if s_x has failed three times
			if counter >= 3:
				panicHaltGracefully("s_x did not recover within three times, I will halt!!!")
			#check that x_now hasn't exceeded x_right
			checkS_right(x_now, gantryLoaded)

			#####################
			x_now = motorR(x_now)
			#####################	

			#checking the result of the motors revolution, has s_x failed
			if x_now==x_start:
				print "s_x failed, gantry did not move!"
				counter=counter+1
			if x_now > x_start:
				x_start=x_now
				counter=0

		if x_next < x_now:
			#check if s_x has failed three times
			if counter >= 3:
				panicHaltGracefully("s_x did not recover within three times, I will halt!!!")

			#check that x_now hasn't exceeded x_right
			checkS_right(x_now, gantryLoaded)

			#####################
			x_now = motorR(x_now)
			#####################	

			#checking the result of the motors revolution, has s_x failed
			if x_now==x_start:
				print "s_x failed, gantry did not move!"
				counter=counter+1
			if x_now < x_start:
				x_start=x_now
				counter=0

		if x_next == x_now:
			print "Gantry on top of object"
			gantryLoaded = toggleMagnet(gantryLoaded)
			return (x_now, gantryLoaded)

# Method that toggles the magnet
def toggleMagnet(gantryLoaded):
	if gantryLoaded == False:
		gantryLoaded = True
		print "Magnet ON"
		simulateMove(2)
		print "Object loaded"
		return gantryLoaded
	else:
		gantryLoaded = False
		print "Magnet OFF"
		simulateMove(2)
		print "Object Unloaded"
		return gantryLoaded

# Method to simulate lag
def simulateMove(x):
	time.sleep(x)
# Motor to move gantry to the left
# have s_x read the new x-value
def motorL(x_now):	
	time.sleep(2)
	print "<"
	return s_x(x_now,"L")
# Motor to move gantry to the right
# have s_x read the new x-value
def motorR(x_now):
	time.sleep(2)
	print ">"
	return s_x(x_now,"R")
# The gantry sensor that returns the x value for the gantrys position
# s_x can fail and produce a number greater than 10, gantry bounds are 0 - 10
def s_x(x_now, direction):
	if x_now=="start" and direction=="":
		x_now_init = random.randint(0,15)	
		return x_now_init
	if direction=="L":
		#Sensor can get stuck, if it recovers after 3 loops the gantry shall continue, othervise it shall halt.
		# 50/50 that it will recover or not
		x = random.randint(0,1)
		if x==1:
			x_now=x_now
		else:
			x_now=x_now
		print "Gantry at x: " + str(x_now)
		return x_now
	if direction=="R":
		#Sensor can get stuck, if it recovers after 3 loops the gantry shall continue, othervise it shall halt.
		# 50/50 that it will recover or not
		x = random.randint(0,1)	
		if x==1:
			x_now=x_now
		else:
			x_now=x_now+1
		print "Gantry at x: " + str(x_now)
		return x_now
# The right sensor
def s_right(x_now):
	if x_now == 10:
		return True
	else: False
# The left sensor, also used as loading bay
def s_left(x_now):
	if x_now == 0:
		return True

	else: False
def panicHalt(gantryLoaded, msg):
	simulateMove(2)
	print msg
	toggleMagnet(gantryLoaded)
	sys.exit()
# halt with the 
def panicHaltGracefully(msg):
	print msg
	sys.exit()
# Method not in use. Should simulate a randomly occuring engine failure. Could be done by utilizing threads!
def enigneFailiure():
	for i in range(random.randint(10,15)):
		time.sleep(1)
	print "Engine malfunction!!!"
	sys.exit()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Example usage: python gantry.py x_next")
	parser.add_argument('x_next', help="Set between 0 and 10")
	args = parser.parse_args()
	x_next = args.x_next
	main(x_next)