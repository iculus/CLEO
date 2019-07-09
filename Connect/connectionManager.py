import sys
sys.path.insert(0,'/home/admin/CLEO/Connect/')
from ssid import *

def getConnStatus(thisName):
	returnNames = visible()
	returnConn, returnKnown = list_()
	mustAdd, mustConnect , DNE = isThisWifiKnown(thisName,returnNames,returnKnown)
	

	activeConns = []
	for index, conn in enumerate(returnConn):
		if conn == "*":
			#print index, conn, returnKnown[index]
			if returnKnown[index] != "Hotspot":
				activeConns.append(returnKnown[index])

	return activeConns, mustAdd, mustConnect, DNE

def connectNow(thisName, thisPass):

	activeConns, mustAdd, mustConnect, DNE = getConnStatus(thisName)
	
	if DNE: print thisName + " Does Not Exist"

	if not DNE: 

		try:deactivate(activeConns)
		except:pass

		print '\nACTIVATING :', thisName, '\n'
	
		print thisName + " Exists"
		print thisName + " must be added     = ", mustAdd
		print thisName + " must be connected = ", mustConnect

		#if mustAdd:
		#	add(thisName,thisPass)

		#if mustConnect:
		#	activate([thisName])

		add(thisName,thisPass)
		activate([thisName])

	activeConns, mustAdd, mustConnect, DNE = getConnStatus(thisName)

	print "\n\nACTIVE CONN :", activeConns, '\n'

if __name__ == "__main__":

	print '\nConnection Manager\n'

	print "available Connections:\n"
	for i in visible():
		print '\t', i
	print '\n'

	sysArgs = (len(sys.argv))

	argList = []
	uLoc = 0	
	pLoc = 0
	for idx in range(sysArgs):
		argList.append(sys.argv[idx])
		if sys.argv[idx] == "-u": uLoc = idx
		if sys.argv[idx] == "-p": pLoc = idx

	sep = " "

	uname = argList [uLoc+1:pLoc]
	pword = argList [pLoc+1:sysArgs]
	#print uname, pword
	user = sep.join(uname)
	passw = sep.join(pword)

	thisName = user
	thisPass = passw

	#print user
	#print passw

	#if sysArgs == 3:
	#thisName = sys.argv[1]
	#thisPass = sys.argv[2]

	#if sysArgs != 3:
	#	thisName = 'Mars'
	#	thisPass = 'frozenbread'

	print thisName, thisPass

	connectNow(thisName, thisPass)


	
	
