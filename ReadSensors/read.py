import sys
sys.path.insert(0,'/home/admin/CLEO/Setup/')
sys.path.insert(0,'/home/admin/CLEO/Sockets/')
sys.path.insert(0,'/home/admin/CLEO/Leap/')

from setup import *
from SensorSetup import getPort, sendIt, setupSerial, readData
import time
from sockets import *
from procCtl import set_procname

print SENSORComputer

print getPort(SENSORComputer)

SENSESerial = setupSerial(SENSORComputer, 115200, 0.01)

start = time.time()
timeout = 0.01

Range = 0
Lux = 0
White = 0
ALS = 0

sensor = "x"
reading = "x"

def interpSensors(inpt,Range,Lux,White,ALS):
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

	return Range,Lux,White,ALS

if __name__ == "__main__":

	#set up socket for sending on ZM0
	port = "5557"
	global senseSocket
	senseSocket = init(port)

	#init serial
	#global ser
	#ser = setupSerial()
	set_procname("crystalz-ard")

	while True:

		now = time.time()	
	
		inpt = readData(SENSESerial)
		Range,Lux,White,ALS=interpSensors(inpt,Range,Lux,White,ALS)

		#send message here on ZM0
		topic = 10001
		messagedata = ":" + str(Range)
		senseSocket.send("%d %s" % (topic, messagedata))

		print time.time() - now
	
		'''
		if now-start > timeout:
		
			print "range : ", int(Range)
			print "Lux   : ", float(Lux)
			print "White : ", float(White)	
			print "ALS   : ", int(ALS)

		'''
