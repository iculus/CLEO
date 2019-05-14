#!/usr/bin/python
# this program takes no input and outputs test patterns to the microcontroller with leds attached

import sys
sys.path.insert(0,'/home/admin/CLEO/Setup/')

from setup import *
from SensorSetup import getPort, sendIt, setupSerial
from numpy import array

print LEDComputer
print SENSORComputer

print getPort(LEDComputer)
print getPort(SENSORComputer)

LEDSerial = setupSerial(LEDComputer)
SENSESerial = setupSerial(SENSORComputer)


testSim = array([	[4,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0],
			[0,0,2,0,0,0,0,0,0,0,0],
			[0,0,0,3,0,0,0,0,0,0,0],
			[0,0,0,0,4,0,0,0,0,0,0],
			[0,0,0,0,0,5,0,0,0,0,0],
			[0,0,0,0,0,0,6,0,0,0,0],
			[0,0,0,0,0,0,0,7,0,0,0],
			[0,0,0,0,0,0,0,0,8,0,0],
			[0,0,0,0,0,0,0,0,0,9,0],
			[0,0,0,0,0,0,0,0,0,0,8],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],	
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0]	])

while True:
	fingerNum = 3
	BRIGHT = 255
	sendIt(testSim,fingerNum,LEDSerial,BRIGHT)
