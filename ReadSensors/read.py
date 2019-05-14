import sys
sys.path.insert(0,'/home/admin/CLEO/Setup/')

from setup import *
from SensorSetup import getPort, sendIt, setupSerial, readData
import time

print SENSORComputer

print getPort(SENSORComputer)

SENSESerial = setupSerial(SENSORComputer)

start = time.time()
timeout = 1

Range = 0
Lux = 0
White = 0
ALS = 0

sensor = "x"
reading = "x"

while True:

	'''
	[u'Range', u' 429\r']
	[u'Lux', u' 160.20\r']
	[u'White', u' 471.85\r']
	[u'Raw ALS', u' 22250\r']
	'''

	now = time.time()	
	
	inpt = readData(SENSESerial)
	if inpt and len(inpt)>2:
		try:
			sensor,reading = inpt.split(":")
		
			if reading > 0:
				if "Range" in sensor: Range = reading
				if "Lux" in sensor: Lux = reading
				if "White" in sensor: White = reading
				if "ALS" in sensor: ALS = reading

		except:
			pass
	
	
	if now-start > timeout:
		
		print "range : ", int(Range)
		print "Lux   : ", float(Lux)
		print "White : ", float(White)	
		print "ALS   : ", int(ALS)

