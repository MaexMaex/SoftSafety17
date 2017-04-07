#!/usr/bin/python
import sys
import argparse
import random
import time

def main(x_next):
	# Magnet starts released
	gantryLoaded = False
	print "#### GANTRY OPERATION TERMINAL 1.0 ####"
	x_next = int(x_next)
	simulateMove(2)
	print "Object at position x: " + str(x_next)
	x_now = s_x()
	print "Gantry at postition x: " + str(x_now)
	simulateMove(2)
	print "Scheaduling pickup!" 
	simulateMove(2)
	(x_now, gantryLoaded) = move(x_next, x_now, gantryLoaded)
	simulateMove(2)
	print "Taking object to loading bay"
	returnToLoadingBay(x_now, gantryLoaded)
# Method triggers the gantry to move back to the loading bay
def returnToLoadingBay(x_now, gantryLoaded):
	bay = s_left(x_now)
	while bay!=True:
		motorL()
		x_now = x_now-1
		# Check with s_left sensor where we are after each move
		bay = s_left(x_now)
		print "Gantry at x: " + str(x_now)
	toggleMagnet(gantryLoaded)
# Movement controller, handels the motors and the magnet
def move(x_next, x_now, gantryLoaded):
	print "Gantry moving"
	while gantryLoaded == False:		
		if x_next > x_now:					
			end = s_right(x_now)
			if end:
				panicHalt()
			motorR()
			x_now=x_now+1
			print "Gantry at x: " + str(x_now)
		if x_next < x_now:
			end = s_left(x_now)	
			if end:
				panicHalt()
			motorL()
			x_now = x_now-1	
			print "Gantry at x: " + str(x_now)
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
def motorL():
	time.sleep(2)
	print "<"
# Motor to move gantry to the right
def motorR():
	time.sleep(2)
	print ">"
# The gantry sensor that returns the x value for the gantrys position
def s_x():
	x_now = random.randint(0,11)
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
def panicHalt():
	simulateMove(2)
	print "Input wants me to go on, but I have reached the end of the boom, I will halt."
	sys.exit()
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Example usage: python gantry.py x_next")
	parser.add_argument('x_next', help="Set between 0 and 10")
	args = parser.parse_args()
	x_next = args.x_next
	main(x_next)