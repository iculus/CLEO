import sys
sys.path.insert(0,'/home/admin/CLEO/Connect/')
from ssid import *

def getActive_():
	actives = []
	active = [x.Connection.GetSettings()['connection']['id'] for x in NetworkManager.NetworkManager.ActiveConnections]
	for i in active:
		if i != 'Hotspot':
			actives.append(i)
	return actives

if __name__ == "__main__":
	returnNames = visible()
	print returnNames
	print getActive_()
