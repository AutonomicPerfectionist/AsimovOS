#from mrlpy import mcommand

class MrlAdapter(object):
	def __init__(self, url, port):
		print "Creating MRL Adapter with master on  %s:%s" % (url, port)
		#mcommand.setURL(url)
		#mcommand.setPort(port)
	def varSet(self, objName, varName, val):
		func = "set" + varName.capitalize()
		print "Executing %s on %s with value %s" % (objName, func, val)
		#mcommand.sendCommand(objName, func, [val])
