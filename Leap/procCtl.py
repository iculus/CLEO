import sys
sys.path.insert(1,'/usr/lib/python2.7')
import subprocess

def startProcess(process):
		return subprocess.call(process, shell=True)

def getPID(processName):
	try:
		return map(int,subprocess.check_output(["pidof",processName]).split())	
	except:
		return 'fail'

def killProcess(processName):
	runningIDS = getPID(processName)
	if len(runningIDS) > 0 and 'fail' not in runningIDS:
		print 'Kill Leapd Processes'
		for i in runningIDS:
			process = "sudo kill -9 " + str(i)
			print process
			print subprocess.call(process, shell=True)
	if 'fail' in runningIDS:
		print 'all good'

def setupProcess(processName, process):
	killProcess(processName)
	return_code = startProcess(process)

def set_procname(newname):
	from ctypes import cdll, byref, create_string_buffer
	libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
	buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
	buff.value = newname                 #Null terminated string as it should be
	libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.

