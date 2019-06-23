import NetworkManager
import sys
import time
import subprocess


def visible():
	returnNames = []
	for device in NetworkManager.NetworkManager.GetDevices():
		if device.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
			continue
		#print("Visible on %s" % device.Udi[device.Udi.rfind('/')+1:])
		device = device.SpecificDevice()
		active = device.ActiveAccessPoint
		aps = device.GetAccessPoints()
		for ap in aps:
			#print ap
			#prefix = '* ' if ap.object_path == active.object_path else '  '
			#print("%s %s" % (prefix, ap.Ssid))
			#print("%s" % (ap.Ssid))
			returnNames.append(ap.Ssid)
	return returnNames

connection_types = ['wireless','wwan','wimax']

def list_():
	knownNames = []
	knownConn = []
	active = [x.Connection.GetSettings()['connection']['id'] for x in NetworkManager.NetworkManager.ActiveConnections]
	connections = [(x.GetSettings()['connection']['id'], x.GetSettings()['connection']['type']) for x in NetworkManager.Settings.ListConnections()]
	fmt = "%%s %%-%ds    %%s" % max([len(x[0]) for x in connections])
	for conn in sorted(connections):
		prefix = '* ' if conn[0] in active else '  '
		#print(fmt % (prefix, conn[0], conn[1]))
		knownConn.append(prefix.replace(' ',''))
		knownNames.append(conn[0])
	return knownConn, knownNames

def deactivate(names):
    active = NetworkManager.NetworkManager.ActiveConnections
    active = dict([(x.Connection.GetSettings()['connection']['id'], x) for x in active])

    for n in names:
        if n not in active:
            print("No such connection: %s" % n, sys.stderr)
            sys.exit(1)

        print("Deactivating connection '%s'" % n)
        NetworkManager.NetworkManager.DeactivateConnection(active[n])

def activate(names):
    connections = NetworkManager.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])

    if not NetworkManager.NetworkManager.NetworkingEnabled:
        NetworkManager.NetworkManager.Enable(True)
    for n in names:
        if n not in connections:
            print("No such connection: %s" % n, sys.stderr)
            sys.exit(1)

        print("Activating connection '%s'" % n)
        conn = connections[n]
        ctype = conn.GetSettings()['connection']['type']

	print ctype 
        if ctype == 'vpn':
            for dev in NetworkManager.NetworkManager.GetDevices():
                if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
                    break
            else:
                print("No active, managed device found", sys.stderr)
                sys.exit(1)
        else:
            dtype = {
                '802-11-wireless': 'wlan',
                'gsm': 'wwan',
            }
            if dtype in connection_types:
                enable(dtype)
            dtype = {
                '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
                '802-3-ethernet': NetworkManager.NM_DEVICE_TYPE_ETHERNET,
                'gsm': NetworkManager.NM_DEVICE_TYPE_MODEM,
            }.get(ctype,ctype)
            devices = NetworkManager.NetworkManager.GetDevices()

            for dev in devices:
                if dev.DeviceType == dtype and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
                    break
            else:
                print("No suitable and available %s device found" % ctype, sys.stderr)
                sys.exit(1)

        NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")

def delete (name):
	print ("Deleting : %s" % name)
	p = subprocess.Popen(["nmcli", "connection", "delete", "id", name], stdout=subprocess.PIPE)
	p.communicate()


def add(name, password):
	print ("Adding : %s" % name)
	p = subprocess.Popen(["nmcli", "dev", "wifi", "con", name, "password", password], stdout=subprocess.PIPE)
	p.communicate()

def findNotKnown(allNames,connNames):
	return np.setdiff1d(allNames,connNames)

def isThisWifiKnown(name,allNames,connNames):
	foundInunknownList = False
	foundInKnownList = False
	doesNotExist = False
	unknown = findNotKnown(allNames,connNames)
	known = connNames
	if name in unknown: foundInunknownList = True
	if name in known: foundInKnownList = True
	if not foundInunknownList and not foundInKnownList: doesNotExist = True
	return foundInunknownList, foundInKnownList, doesNotExist

def getActive():
	actives = []
	active = [x.Connection.GetSettings()['connection']['id'] for x in NetworkManager.NetworkManager.ActiveConnections]
	for i in active:
		if i != 'Hotspot':
			actives.append(i)
	return actives		


import numpy as np

if __name__ == "__main__":
	print "TESTING \n\nVisible"
	returnNames = visible()
	print '\n', returnNames
	time.sleep(3)
	print "\n\nKnown"	
	returnConn, returnKnown = list_()
	print '\n',returnConn,'\n',returnKnown

	print "\n\nFound but not known\n\n"
	notKnown = findNotKnown(returnNames,returnKnown)
	print notKnown

	print '\n\nKNOWN WIFI\n\n'
	thisName = 'lupaupa'
	mustAdd, mustConnect , DNE = isThisWifiKnown(thisName,returnNames,returnKnown)
	print thisName + "must be added     = ", mustAdd
	print thisName + "must be connected = ", mustConnect
	if DNE: print thisName + " Does Not Exist"
	if not DNE: print thisName + " Exists"

	print "\n\n\nDEACTIVATE\n"
	deactivate(["Mars"])
	time.sleep(3)
	list_()
	print "\n\n\nACTIVATE\n"
	activate(["Mars"])
	time.sleep(3)
	list_()
	print "\n\nDELETE\n"
	delete('Mars')
	time.sleep(5)
	list_()
	print "\n\nUNDELETE\n"
	add('Mars','frozenbread')
	time.sleep(3)
	list_()

