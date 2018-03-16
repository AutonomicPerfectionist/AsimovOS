import socket
from configobj import ConfigObj

class AsimovConfig:
	def __init__(self, path="/etc/asimov-local/"):
		if not path.endswith('/'):
			path += '/'
		self.path = path
		self.conf = ConfigObj(path + "asimov.conf" )
	def getTrimmedPropList(self, section, prop):
		ret = self.conf[section][prop]
		for i in range(0, len(ret)):
			ret[i] = ret[i].strip()
		return ret

	def getNodeTypes(self):
		return self.conf["cluster"]["types"].keys()
	
	def getInterfaces(self):
		return self.conf["system"]["interfaces"]
	
	def getNodeTypeParams(self, type):
		return self.conf["cluster"]["types"][type]

	def getBootRequirements(self):
		return self.getTrimmedPropList("requirements", "boot")

	def getShutdownRequirements(self):
		return self.getTrimmedPropList("requirements", "shutdown")

	def getCapabilityPath(self):
		return self.conf["capabilities"]["path"].strip()

	def getClusterName(self):
		return self.conf["cluster"]["name"]

	def getHostname(self):
		if self.conf["system"]["hostname"] == "DEFAULT":
			return socket.gethostname() + ".local"
		else:
			return self.conf["system"]["hostname"]
	def getConf(self):
		return self.conf
