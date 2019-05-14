from numpy import interp

def returnCalibratedPosition(uncalPos, sensorMin, sensorMax, lightMin, lightMax):
	calibrated = clamp(uncalPos,sensorMin,sensorMax)
	calibrated = int( interp(calibrated,[sensorMin,sensorMax],[lightMin,lightMax]) )
	return calibrated

def clamp(n, minn, maxn):
    return max(min(n, maxn), minn)
