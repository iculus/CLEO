import zmq
import threading

class listenThread(threading.Thread):

	def __init__(self, name='listenThread', group='thread', target='target'):
		""" constructor, setting initial variables """
		self._stopevent = threading.Event(  )
		self._sleepperiod = 0.1
		self.topic = "NONE"
		self.messagedata = "NONE"
		self.socket = 0
		threading.Thread.__init__(self, name=name)

	def run(self):
		""" main control loop """
		while not self._stopevent.isSet(  ):
			string = self.socket.recv()
			self.messagedata = string

	def join(self, timeout=None):
		""" Stop the thread. """
		print "exiting", self.name
		self._stopevent.set(  )
		threading.Thread.join(self, timeout)

	def __str__(self):
		""" info to send back to main process """
		return str(self.messagedata)
		
def setupListenSocket(port = "5556" ,topicfilter = "0000"):
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect ("tcp://localhost:%s" % port)
	socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
	return socket
	
def startThreads(socket, thread):
	lThread = thread
	lThread.socket = socket
	lThread.daemon = True
	lThread.start()
	return lThread
	
def sendMessage(topic = 10001, messagedata = 123, socket=0):
	socket.send("%d %d" % (topic, messagedata))
	
def init(port):
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://*:%s" % port)
	return socket
