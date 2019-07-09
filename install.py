# install system
import os, stat

def getSetup():
	data = ""
	try:
		with open('/home/admin/setup.CLEO') as theFile:
			data = theFile.readlines()
	except: pass

	name=number=ngrokhttp=ngroktcp=password=ip=wifipassword=""

	for i in data:
		typ, val = i.split("=")
		val = val.strip('\n')
		print typ, val
		if "name" in typ: name = val
		if "number" in typ: number = val
		if "http" in typ: ngrokhttp = val
		if "tcp" in typ: ngroktcp = val
		if "password" in typ and "wifi" not in typ: password = val
		if "ip" in typ: ip = val
		if "wifi" in typ: wifipassword = val

	return name, number, ngrokhttp, ngroktcp, password, ip, wifipassword


name, number, ngrokhttp, ngroktcp, password, ip, wifipassword = getSetup()

print "\n-"+password+"-\n"

number = raw_input("Please enter CLEO number ["+number+"]: ") or number
name = "CLEO "+ number
print "\n\twelcome: ", name, '\n'

ngrokhttp = raw_input("please enter NGROK HTTP address ["+ngrokhttp+"]: ") or ngrokhttp
print "\n\ttcp address: ", ngrokhttp, '\n'

ngroktcp = raw_input("please enter NGROK TCP address ["+ngroktcp+"]: ") or ngroktcp
print "\n\thttp address: ", ngroktcp, '\n'

password = raw_input("please enter administrative password ["+password+"]: ") or password
print "\n\tpassword: ", password, '\n'

ip = "10.42.0." + number

acceptip = raw_input("accept default ip " + ip + " y/n: ")
if acceptip == "y" or acceptip == "Y": print '\n\taccepted'
if acceptip == "n" or acceptip == "N": ip = raw_input("please enter desired ip ["+ip+"]: ") or ip

print "\n\tIP: ", ip, '\n'

wifipassword = raw_input("please enter desired wifi password ["+wifipassword+"]: ") or wifipassword
print "\n\twifi password: ", wifipassword, '\n'




with open('/home/admin/setup.CLEO', 'w') as theFile:
	theFile.write("name="+name+'\n')
	theFile.write("number="+number+'\n')
	theFile.write("http="+ngrokhttp+'\n')
	theFile.write("tcp="+ngroktcp+'\n')
	theFile.write("password="+password+'\n')
	theFile.write("ip="+ip+'\n')
	theFile.write("wifi="+wifipassword+'\n')

#generate ngrok files here

currentPath = "/home/admin/"
newPath = currentPath+"CLEO/Launcher/"

grokTCP = currentPath+'grok.sh'
grokHTTP = currentPath+'grokweb.sh'

with open(grokTCP, 'w') as grokTCPFile:
	grokTCPFile.write("#!/bin/sh\n")
	grokTCPFile.write("\n")
	grokTCPFile.write("#"+name+"\n")
	grokTCPFile.write("/home/admin/ngrok tcp 22 -remote-addr="+ngroktcp+"\n")
	grokTCPFile.write("\n")
	grokTCPFile.write("exit 0\n")

with open(grokHTTP, 'w') as grokHTTPFile:
	grokHTTPFile.write("#!/bin/sh\n")
	grokHTTPFile.write("\n")
	grokHTTPFile.write("#"+name+"\n")
	grokHTTPFile.write("/home/admin/ngrok http -subdomain "+ngrokhttp.split(".")[0]+" 80 \n")
	grokHTTPFile.write("\n")
	grokHTTPFile.write("exit 0\n")

def setPermissions(fileToSet):
	st = os.stat(fileToSet)
	os.chmod(fileToSet, 0775)

setPermissions(grokTCP)
setPermissions(grokHTTP)

os.rename(currentPath+'grok.sh', newPath+'grok.sh')
os.rename(currentPath+'grokweb.sh', newPath+'grokweb.sh')




