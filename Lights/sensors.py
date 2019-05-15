def map(x, in_min, in_max, out_min, out_max):
			return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

		
def sensors(senseThread):

	'''get the sensors data'''
	
	ranger = 0
	reading = False
	distanceMin = 10
	distanceMax = 1200
	timeoutCounter = 0
	person = False
	personNearby = False
	d = 0

	#clean the thread update
	if str(senseThread) != "NONE":
		topic, ranger = str(senseThread).replace(" ", "").split(":")
	
	#map ranger to steps
	rangerMin = 0
	rangerMax = 7

	ranger = int(ranger)

	if ranger > 8180 and ranger < 8200:
		reading = False

	elif ranger <= distanceMax:
		reading = True	
		timeoutCounter = 0	
		d = map(ranger, distanceMin, distanceMax, rangerMin, rangerMax)
	
	#check for people
	if d > 1 and d < 7 and reading == True:
		personNearby = True
	elif d <= 1 or d >= 7 and reading == True:
		personNearby = False
	elif reading == False:
		timeoutCounter = timeoutCounter + 1
		if timeoutCounter > 20:
			timeoutCounter = 0
			personNearby = False
	#if reading == True:
	return reading, personNearby, ranger, d
